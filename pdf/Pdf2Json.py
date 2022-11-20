import string
from typing import final
from collections import deque
import json
import pdfplumber
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import *
from SelectedStack import SelectedStack
from DataType import *
from Default import *


class Pdf2Json:
    def __init__(self, _FileSet : list):
        self.MAX_COUNT : final = 100                # max pending counting
        self.FileSet = _FileSet
        self.TextList = deque()                          # list of TextLine
        self.CellList = deque()
        self.TopicList = [] 

    def pdf_to_data(self):
        for file in self.FileSet:
            self.read_pdf(file)
            self.textline_layering()
            self.divide_by_topic()
            
            with open('output.json', 'w', encoding="utf-8") as output:
                json.dump(self.TopicList, output, ensure_ascii=False, indent='\t')   

    def read_pdf(self, FileString : string):
        with open(FileString, 'rb') as input_file:
            with pdfplumber.PDF(input_file) as pdf_file:
                for page_miner, page_plumber in zip(extract_pages(input_file), pdf_file.pages):
            
                    chars_plumber = page_plumber.chars
                    index = 0                       # index for indicating character page_plumber
                    page_default_color = pick_default_color(chars_plumber)
                    bold_check = need_bold_check(chars_plumber)
                    
                    page_number = page_plumber.page_number
                    
                    textlines = []
                    pending_list = []
                    # list of pending_textline
                    # for unmatched textline between pdfminer and pdfplumber
                    pending_count = 0 

                    for element in page_miner:
                        if isinstance(element, LTTextBox):
                            for textline in element:
                                if isinstance(textline, LTTextLine):
                                    textlines.append(textline.get_text())
                                    
                    
                    while textlines or pending_list:
                        if textlines:
                            textline = textlines.pop(0)
                        else:
                            textline = pending_list.pop(0)
                            pending_count += 1

                        if textline[0] == chars_plumber[index]['text']:
                            try:
                                index = self.detect_diff(chars_plumber, textline, index, page_number, page_default_color, bold_check)
                            except: 
                                pending_list.append(textline)
                                continue
                
                        else:
                            pending_list.append(textline) 
                            for pending_index in range(len(pending_list)):
                                if pending_list[pending_index][0] == chars_plumber[index]['text']:    
                                    pending_textline = pending_list.pop(pending_index)
                                    try:
                                        index = self.detect_diff(chars_plumber, pending_textline, index, page_number, page_default_color, bold_check)
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
                    print('pdf extracion is not perfect !!')
            


    def detect_diff(self, chars, textline, index, page_num, default_color, bold_check):
        # keyword checking stacks
        ColorDiffStack = SelectedStack()
        BoldDiffStack = SelectedStack()
        # keyword checking status
        ColorKeyword = False
        BoldKeyword = False

        current_color = default_color
                        
        size = 0
        location = 0
        if textline[0] == ' ':
            textline = textline.lstrip()
        while chars[index]['text'] == ' ':
            index += 1
            
        if self.is_special_symbol(chars[index]['text']):
            size = chars[index+1]['size']
            location = chars[index+1]['x0']
        else:
            size = chars[index]['size']
            location = chars[index]['x0']
        keyword_set = []

        for char_miner in textline:
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
                if 'Bold' in chars[index]['fontname'] and not BoldKeyword and not ColorKeyword and bold_check:
                    BoldKeyword = True
                    BoldDiffStack.push(char_miner)
                # continue keyword searching
                elif 'Bold' in chars[index]['fontname'] and BoldKeyword and bold_check:
                    BoldDiffStack.push(char_miner)
                # stop keyword searching
                elif 'Bold' not in chars[index]['fontname'] and BoldKeyword and bold_check:
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
            
        self.TextList.append(TextLine(textline,size,location,keyword_set,page_num))
        return index

    # 해당 input이 특수문자인지 확인
    def is_special_symbol(self, input):
        if 48 <= ord(input) <= 57:
            return False
        elif 65 <= ord(input) <= 90:
            return False  
        elif 97 <= ord(input) <= 122:
            return False  
        elif 44032 <= ord(input) <= 55215:
            return False  
        elif ord(input) == 10 or ord(input) == 32 or ord(input) == 34 or ord(input) == 39 or ord(input) == 40 or ord(input) == 8220:
            return False
        else:
            return True
       
    # TextLine을 Cell로 바꾸기
    def textline_layering(self):
        cell_text = self.TextList.popleft()
        current_page_cells = []
        current_page_cells.append(cell_text)
        
        current_page = cell_text.page_num
        max_size = cell_text.size
        index = 0
        max_index = index
        
        while self.TextList:
            if self.TextList[0].page_num == current_page:
                cell_text = self.TextList.popleft()
                # combine
                if index > 0:
                    if not self.is_special_symbol(cell_text.text[0]):
                        if abs(cell_text.size-current_page_cells[index-1].size) < 0.1 and abs(cell_text.location - current_page_cells[index-1].location) < cell_text.size/2:
                            current_page_cells[index-1].text = current_page_cells[index-1].text.strip() + " " + cell_text.text.strip()
                            current_page_cells[index-1].keyword_set.extend(cell_text.keyword_set)
                            continue
                        
                        elif abs(cell_text.size-current_page_cells[index-1].size) < 0.1 and len(current_page_cells[index-1].text) == 1:
                            current_page_cells[index-1].text = current_page_cells[index-1].text.strip() + " " + cell_text.text.strip()
                            current_page_cells[index-1].keyword_set.extend(cell_text.keyword_set)
                            continue
                        
                        elif abs(cell_text.size-current_page_cells[index-1].size) < cell_text.size/3  and abs(cell_text.location - current_page_cells[index-1].location) < cell_text.size:
                            current_page_cells[index-1].text = current_page_cells[index-1].text.strip() + "\n" + cell_text.text.strip()
                            current_page_cells[index-1].keyword_set.extend(cell_text.keyword_set)
                            continue
                        
                        else:
                            pass
                             
                if len(cell_text.text.strip()) == 1:
                    if self.is_special_symbol(cell_text.text.strip()):
                        cell_text.text = cell_text.text.strip()
                    else:
                        continue
                    
                current_page_cells.append(cell_text)
                if cell_text.size > max_size:
                    max_size = cell_text.size
                    max_index = index      
                index += 1
            else:
                max_cell_text = current_page_cells.pop(max_index)
                max_cell = {'topic' : max_cell_text.text.strip(), 'keywords' : max_cell_text.keyword_set, 'page' : [max_cell_text.page_num],'sentences' : []}
    
                # layering 
                while current_page_cells:
                    temp = current_page_cells.pop(0)
                    cur_size = temp.size
                    cur_loc = temp.location
                    cur_cell = {'text' : temp.text, 'keywords' : temp.keyword_set, 'sentences' : []}
                    max_cell['sentences'].append(cur_cell) 
                    return_code = self.layering(max_cell, cur_cell, cur_size, cur_loc, current_page_cells)
                    
                    if return_code == -1:
                        break 
                
                self.CellList.append(max_cell)
    
                cell_text = self.TextList[0]
                current_page = cell_text.page_num
                max_size = cell_text.size
                index = 0
                max_index = index
                
                
        if current_page:
            max_cell_text = current_page_cells.pop(max_index)
            max_cell = {'topic' : max_cell_text.text, 'keywords' : max_cell_text.keyword_set, 'page' : [max_cell_text.page_num],'sentences' : []}

            # layering 
            while current_page_cells:
                temp = current_page_cells.pop(0)
                cur_size = temp.size
                cur_loc = temp.location
                cur_cell = {'text' : temp.text, 'keywords' : temp.keyword_set, 'sentences' : []}
                max_cell['sentences'].append(cur_cell) 
                return_code = self.layering(max_cell, cur_cell, cur_size, cur_loc, current_page_cells)
                
                if return_code == -1:
                    break 
            
            self.CellList.append(max_cell)
            
    
    # RETURN CODE
    # -1 : empty list
    # 0 : terminate layering
    # 1 : return to caller 
    def layering(self, parent_cell, cur_cell, cur_size, cur_loc, page_cells):
        if len(page_cells) == 0:
            return -1

        temp = page_cells[0]
        if self.is_special_symbol(temp.text[0]):
            if abs(temp.size - cur_size) < 1 and abs(temp.location - cur_loc) < temp.size/5:
                temp = page_cells.pop(0)
                temp_cell = {'text' : temp.text, 'keywords' : temp.keyword_set, 'sentences' : []}
                parent_cell['sentences'].append(temp_cell)
                return_code = self.layering(parent_cell, temp_cell, temp.size, temp.location, page_cells)
                if return_code == 1:
                    return 1
                
            elif (temp.size <= cur_size or abs(temp.size - cur_size) < 0.1) and temp.location > cur_loc:
                temp = page_cells.pop(0)
                temp_cell = {'text' : temp.text, 'keywords' : temp.keyword_set, 'sentences' : []}
                cur_cell['sentences'].append(temp_cell)
                return_code = self.layering(cur_cell, temp_cell, temp.size, temp.location, page_cells)
                if return_code == 1:
                    if abs(page_cells[0].size - cur_size) < 1 and abs(page_cells[0].location - cur_loc) < 0.1:
                        temp = page_cells.pop(0)
                        temp_cell = {'text' : temp.text, 'keywords' : temp.keyword_set, 'sentences' : []}
                        parent_cell['sentences'].append(temp_cell)
                        return_code = self.layering(parent_cell, temp_cell, temp.size, temp.location, page_cells)
                        if return_code == 1:
                            return 1
                                
                    elif page_cells[0].size >= cur_size and page_cells[0].location < cur_loc:
                        return 1 
                    else: 
                        return 0
                
            elif temp.size >= cur_size and temp.location < cur_loc:
                return 1
            
            else:
                return 0
        else:
            return 0
        
    def divide_by_topic(self):
        self.TopicList.append(self.CellList.popleft())
    
        while self.CellList:
            temp = self.CellList.popleft()
            if temp['topic'] == self.TopicList[-1]['topic']:
                self.TopicList[-1]['sentences'].extend(temp['sentences'])
                self.TopicList[-1]['page'].extend(temp['page'])
                
            else:
                self.TopicList.append(temp)
                
            

       
            
   
   
 