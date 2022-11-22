import string
from typing import final
import pdfplumber
from pdfminer.high_level import extract_pages
from pdfminer.layout import *
from SelectedStack import SelectedStack
from DataType import *
from Default import *
from io import BytesIO


class Pdf2Json:
    def __init__(self, _FileSet: list):
        self.MAX_COUNT: final = 300  # max pending counting
        self.FileSet = _FileSet
        self.data = []
        self.TextList = []  # list of TextLine
        self.combined_TextList = []  # list of TextLine
        self.ThemeList = []  # list of Theme

    def pdf_to_json(self):
        for file in self.FileSet:
            self.read_pdf(file)
            self.combine()
            self.divide_by_theme(self.combined_TextList)
            self.write_json()

            self.TextList.clear()
            self.combined_TextList.clear()
            self.ThemeList.clear()

    def read_pdf(self, FileString: string):
        input_file = BytesIO(FileString)
        with pdfplumber.PDF(input_file) as pdf_file:
            for page_miner, page_plumber in zip(extract_pages(input_file), pdf_file.pages):

                chars_plumber = page_plumber.chars
                index = 0  # index for indicating character page_plumber
                page_default_color = pick_default_color(chars_plumber)
                page_number = page_plumber.page_number

                textlines = []
                # list of pending_textline
                # for unmatched textline between pdfminer and pdfplumber
                pending_list = []
                pending_count = 0

                box_num = 0
                for element in page_miner:
                    if isinstance(element, LTTextBox):
                        for textline in element:
                            if isinstance(textline, LTTextLine):
                                textlines.append({'text': textline.get_text(), 'box number': box_num})
                        box_num += 1

                while textlines or pending_list:
                    if textlines:
                        textline = textlines.pop(0)
                    else:
                        textline = pending_list.pop(0)
                        pending_count += 1

                    if textline['text'][0] == chars_plumber[index]['text']:
                        try:
                            index = self.detect_diff(chars_plumber, textline, index, page_number, page_default_color)
                        except:
                            pending_list.append(textline)
                            continue

                    else:
                        pending_list.append(textline)
                        for pending_index in range(len(pending_list)):
                            if pending_list[pending_index]['text'][0] == chars_plumber[index]['text']:
                                pending_textline = pending_list.pop(pending_index)
                                try:
                                    index = self.detect_diff(chars_plumber, pending_textline, index, page_number,
                                                             page_default_color)
                                except:
                                    pending_list.append(pending_textline)
                                break
                            else:
                                continue

                    if pending_count > self.MAX_COUNT:
                        break

                if pending_list:
                    pending_list.clear()
                    print(page_plumber.page_number)
                    print('pdf extraction is not perfect !!')

    def write_json(self):
        for theme in self.ThemeList:
            theme_dic = {'Theme': '', 'Texts': []}
            textline_dic = {'Text': '', 'Keyword': []}

            theme_dic['Theme'] = theme.quiver
            for arrow in theme.arrows.array:
                textline_dic['Text'] = arrow.text
                textline_dic['Keyword'].extend(arrow.keyword_set)
                theme_dic['Texts'].append(textline_dic)

                textline_dic = {'Text': '', 'Keyword': []}

            self.data.append(theme_dic)


    def detect_diff(self, chars, textline, index, page_num, default_color):
        # keyword checking stacks
        ColorDiffStack = SelectedStack()
        BoldDiffStack = SelectedStack()
        # keyword checking status
        ColorKeyword = False
        BoldKeyword = False

        current_color = default_color
        
        keyword_set = []
        size = chars[index]['size']
        location = chars[index]['x0']
        for char_miner in textline['text']:
            if char_miner == chars[index]['text']:
                # COLOR
                # start keyword searching 
                if current_color != str(chars[index]['non_stroking_color']) and not ColorKeyword and not BoldKeyword:
                    current_color = str(chars[index]['non_stroking_color'])
                    ColorKeyword = True
                    ColorDiffStack.push(char_miner)
                # continue keyword searching
                elif current_color == str(chars[index]['non_stroking_color']) and ColorKeyword:
                    ColorDiffStack.push(char_miner)
                # stop keyword searching
                elif current_color != str(chars[index]['non_stroking_color']) and ColorKeyword:
                    current_color = str(chars[index]['non_stroking_color'])
                    ColorKeyword = False
                    keyword_set.append(ColorDiffStack.pop_all())
                    
                else:
                    pass

                # FONT
                # start keyword searching 
                if 'Bold' in chars[index]['fontname'] and not BoldKeyword and not ColorKeyword:
                    BoldKeyword = True
                    BoldDiffStack.push(char_miner)
                # continue keyword searching
                elif 'Bold' in chars[index]['fontname'] and BoldKeyword:
                    BoldDiffStack.push(char_miner)
                # stop keyword searching
                elif 'Bold' not in chars[index]['fontname'] and BoldKeyword:
                    BoldKeyword = False
                    keyword_set.append(BoldDiffStack.pop_all())

                    
                    if current_color != str(chars[index]['non_stroking_color']) and not ColorKeyword and not BoldKeyword:
                        current_color = str(chars[index]['non_stroking_color'])
                        ColorKeyword = True
                        ColorDiffStack.push(char_miner)
                else:
                    pass
                
                if index < len(chars)-1:
                    index += 1

            else:
                if ColorKeyword:
                    if char_miner == '\n':
                        current_color = default_color
                        ColorKeyword = False
                        keyword_set.append(ColorDiffStack.pop_all())             
                    elif char_miner == ' ':
                        ColorDiffStack.push(' ')
                    else:
                        raise Exception('mismatching detected!!')
                    
                elif BoldKeyword:
                    if char_miner == '\n':
                        BoldKeyword = False
                        keyword_set.append(BoldDiffStack.pop_all())
                    elif char_miner == ' ':
                        BoldDiffStack.push(' ')
                    else:
                        raise Exception('mismatching detected!!')
                else:
                    if char_miner == '\n' or char_miner == ' ':
                        continue
                    else:
                        raise Exception('mismatching detected!!')

        self.TextList.append(TextLine(textline['text'],size,location,keyword_set,page_num,textline['box number']))
        return index

    def combine(self):
        combined_textline = self.TextList.pop(0)
        current_page = combined_textline.page_num
        current_box = combined_textline.box_num

        combined_text = []
        combined_text.append(combined_textline.text.strip())
        while self.TextList:
            if self.TextList[0].page_num == current_page and self.TextList[0].box_num == current_box:
                temp = self.TextList.pop(0)  
                temp.text = temp.text.strip()
                if 48 <= ord(temp.text[0]) <= 57:
                    temp.text = ' ' + temp.text  
                elif 65 <= ord(temp.text[0]) <= 90:
                    temp.text = ' ' + temp.text  
                elif 97 <= ord(temp.text[0]) <= 122:
                    temp.text = ' ' + temp.text  
                elif 44032 <= ord(temp.text[0]) <= 55215:
                    temp.text = ' ' + temp.text  
                else:
                    temp.text = '\n' + temp.text
                
                combined_text.append(temp.text)
                combined_textline.keyword_set.extend(temp.keyword_set)
 
            else:
                temp_text = "".join(combined_text)

                combined_textline.text = temp_text
                self.combined_TextList.append(combined_textline)

                combined_textline = self.TextList.pop(0)
                current_page = combined_textline.page_num
                current_box = combined_textline.box_num           
                combined_text.clear()
                combined_text.append(combined_textline.text.strip())
                

    def divide_by_theme(self, TextList):
        next_page_num = 1
        while TextList:
            current_page_num = TextList[0].page_num
            max_font_size = 0
            arrows = Arrows()
            theme = Theme("", arrows)

            while current_page_num == next_page_num:
                textline = TextList.pop(0)
                if max_font_size < textline.size:
                    max_font_size = textline.size
                    theme.quiver = textline.text

                theme.arrows.add(Arrow(textline.text, textline.keyword_set))
                if TextList:
                    next_page_num = TextList[0].page_num
                else:
                    break

            is_present_quiver = False
            if self.ThemeList:
                for set_theme in self.ThemeList:
                    if set_theme.quiver == theme.quiver:
                        is_present_quiver = True
                        set_theme.arrows.array.extend(theme.arrows.array)

                if is_present_quiver:
                    pass
                else:
                    self.ThemeList.append(theme)

            else:
                self.ThemeList.append(theme)