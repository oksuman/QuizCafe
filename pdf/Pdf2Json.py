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
        self.MAX_COUNT : final = 30                      # max pending counting
        self.FileSet = _FileSet
        self.TextList = deque()                          # list of TextLine
        self.CellList = deque()
        self.TopicList = [] 
        self.color_list = {}
        self.page_height = 0

    def pdf_to_data(self):
        for file in self.FileSet:
            self.color_list = {}
            file_name = self.read_pdf(file)
            self.textline_layering()
            self.divide_by_topic()
            for topic in self.TopicList:
                topic['file'] = file_name
            
            with open('output.json', 'w', encoding="utf-8") as output:
                json.dump(self.TopicList, output, ensure_ascii=False, indent='\t')   

    def read_pdf(self, FileString : string):
        with open(FileString, 'rb') as input_file:
            file_name = input_file.name
            with pdfplumber.PDF(input_file) as pdf_file:
                for page_miner, page_plumber in zip(extract_pages(input_file), pdf_file.pages):
                    
                    chars_plumber = page_plumber.chars
                    index = 0                       # index for indicating character page_plumber

                    
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
                                    
                    if textlines:
                        page_default_color = pick_default_color(chars_plumber, self.color_list)
                        bold_check = need_bold_check(chars_plumber)
                        self.page_height = page_plumber.height
                        page_number = page_plumber.page_number

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

        return file_name

    def detect_diff(self, chars, textline, index, page_num, default_color, bold_check):
        current_color = default_color
        # keyword checking stacks
        ColorDiffStack = SelectedStack()
        BoldDiffStack = SelectedStack()
        # keyword checking status
        ColorKeyword = False
        BoldKeyword = False
        head_keyword = False
        tail_keyword = False
        symbol_start = False 
        keyword_set = []

        textline = textline.lstrip()
        while chars[index]['text'] == ' ':
            index += 1

        cursor = 0  # cursor that indicate miner text 
        end_point = len(textline)
        state = 0

        size = 0
        x0 = chars[index]['x0'] 
        x1 = 0
        y0 = chars[index]['y0']
        
        if self.is_special_symbol(chars[index]['text']) == 0:
            size = chars[index]['size']
            state = 1 
        elif self.is_special_symbol(chars[index]['text']) == 1:
            x1 = chars[index]['x0'] 
            size = chars[index]['size']
        elif self.is_special_symbol(chars[index]['text']) == 3:
            symbol_start = True
            size = chars[index]['size']
            state = 2

        for char_miner in textline:
            if char_miner == chars[index]['text']:

                if state == 1:
                    if self.is_special_symbol(chars[index]['text']) == 1:
                        x1 = x0
                        state = 0
                    elif self.is_special_symbol(chars[index]['text']) == 3:
                        symbol_start = True
                        state = 2
                if state == 2:
                    if self.is_special_symbol(chars[index]['text']) == 1:
                        x1 = chars[index]['x0']
                        state = 0
        
                # COLOR
                # start keyword searching 
                if current_color != str(chars[index]['non_stroking_color']) and not ColorKeyword and not BoldKeyword:
                    current_color = str(chars[index]['non_stroking_color'])
                    ColorKeyword = True
                    ColorDiffStack.push(char_miner)
                    if cursor == 0:
                        head_keyword = True
                # continue keyword searching
                elif current_color == str(chars[index]['non_stroking_color']) and ColorKeyword:
                    ColorDiffStack.push(char_miner)
                # stop keyword searching
                elif current_color != str(chars[index]['non_stroking_color']) and ColorKeyword:
                    current_color = str(chars[index]['non_stroking_color'])
                    ColorKeyword = False
                    keyword_set.append(ColorDiffStack.pop_all())
                    if cursor == end_point - 1:
                        tail_keyword = True 
                else:
                    pass

                # FONT
                # start keyword searching 
                if 'Bold' in chars[index]['fontname'] and not BoldKeyword and not ColorKeyword and bold_check:
                    BoldKeyword = True
                    BoldDiffStack.push(char_miner)
                    if cursor == 0:
                        head_keyword = True
                # continue keyword searching
                elif 'Bold' in chars[index]['fontname'] and BoldKeyword and bold_check:
                    BoldDiffStack.push(char_miner)
                # stop keyword searching
                elif 'Bold' not in chars[index]['fontname'] and BoldKeyword and bold_check:
                    BoldKeyword = False
                    keyword_set.append(BoldDiffStack.pop_all())
                    if cursor == end_point - 1:
                        tail_keyword = True 

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
                        tail_keyword = True         
                    elif char_miner == ' ':
                        ColorDiffStack.push(' ')
                    else:
                        raise Exception('mismatching detected!!')
                    
                elif BoldKeyword:
                    if char_miner == '\n':
                        BoldKeyword = False
                        keyword_set.append(BoldDiffStack.pop_all())
                        tail_keyword = True 
                    elif char_miner == ' ':
                        BoldDiffStack.push(' ')
                    else:
                        raise Exception('mismatching detected!!')
                else:
                    if char_miner == '\n' or char_miner == ' ':
                        continue
                    elif chars[index]['text'] == ' ':
                        index+=1
                    else:
                        raise Exception('mismatching detected!!')

            cursor += 1
        if self.page_height/10 - size < y0 < self.page_height/10 * 9 + size:
            self.TextList.append(TextLine(textline, size, x0, x1, y0, keyword_set, page_num, head_keyword, tail_keyword, symbol_start))
        return index
       
    # TextLine을 Cell로 바꾸기
    def textline_layering(self):
        cell_text = self.TextList.popleft()
        current_page_cells = []
        current_page_cells.append(cell_text)
        
        current_page = cell_text.page_num
        max_size = cell_text.size
        max_y = cell_text.y0
        index = 0
        max_index = index
        
        while self.TextList:
            if self.TextList[0].page_num == current_page:
                cell_text = self.TextList.popleft()
                # combine
                if index > 0:
                    if not cell_text.symbol_start:
                        if abs(cell_text.size-current_page_cells[index-1].size) < 0.1 and abs(cell_text.x1 - current_page_cells[index-1].x1) < cell_text.size/5 and abs(cell_text.y0 - current_page_cells[index-1].y0) < 3*cell_text.size:
                            # 잘린 키워드
                            if current_page_cells[index-1].tail_keyword and cell_text.head_keyword:
                                current_page_cells[index-1].text = current_page_cells[index-1].text.strip()  + cell_text.text.strip()
                                combined_keyword = current_page_cells[index-1].keyword_set.pop() + cell_text.keyword_set.pop(0)
                                current_page_cells[index-1].keyword_set.append(combined_keyword)
                                current_page_cells[index-1].keyword_set.extend(cell_text.keyword_set)
                            else:
                                current_page_cells[index-1].text = current_page_cells[index-1].text.strip() + " " + cell_text.text.strip()
                                current_page_cells[index-1].keyword_set.extend(cell_text.keyword_set)
                            current_page_cells[index-1].y0 = cell_text.y0
                            continue
                        
                        # and len(current_page_cells[index-1].text) == 1 
                        elif abs(cell_text.size-current_page_cells[index-1].size) < 0.1 and abs(current_page_cells[index-1].y0-cell_text.y0) < 0.1:
                            current_page_cells[index-1].text = current_page_cells[index-1].text.strip() + " " + cell_text.text.strip()
                            # 잘린 키워드
                            if current_page_cells[index-1].tail_keyword and cell_text.head_keyword:
                                combined_keyword = current_page_cells[index-1].keyword_set.pop() + cell_text.keyword_set.pop(0)
                                current_page_cells[index-1].keyword_set.append(combined_keyword)
                            current_page_cells[index-1].keyword_set.extend(cell_text.keyword_set)
                            current_page_cells[index-1].x1 = cell_text.x1
                            continue
                        
                        elif abs(cell_text.size-current_page_cells[index-1].size) < cell_text.size/3  and abs(cell_text.x1 - current_page_cells[index-1].x1) < cell_text.size and abs(cell_text.y0 - current_page_cells[index-1].y0) < 3* cell_text.size:
                            current_page_cells[index-1].text = current_page_cells[index-1].text.strip() + "\n" + cell_text.text.strip()
                            current_page_cells[index-1].keyword_set.extend(cell_text.keyword_set)
                            continue
                        
                        else:
                            pass
                             
                if len(cell_text.text.strip()) == 1:
                    if self.is_special_symbol(cell_text.text.strip()) == 3:
                            if cell_text.text.strip() == '.':
                                continue
                            else:
                                cell_text.text = cell_text.text.strip()
                    else:
                        continue
                    
                current_page_cells.append(cell_text)
                if cell_text.size > max_size and cell_text.y0 > self.page_height/2:
                    if cell_text.y0 < max_y and abs(cell_text.size - max_size) < 0.1:
                        pass
                    else:
                        max_size = cell_text.size
                        max_index = index      
                index += 1
            else:
                max_cell_text = current_page_cells.pop(max_index)
                max_cell = {'topic' : max_cell_text.text.strip(), 'keywords' : max_cell_text.keyword_set,'file' : "" ,'page' : [max_cell_text.page_num],'sentences' : []}
    
                # layering 
                while current_page_cells:
                    temp = current_page_cells.pop(0)
                    cur_size = temp.size
                    cur_loc = temp.x0
                    cur_cell = {'text' : temp.text, 'keywords' : temp.keyword_set, 'sentences' : []}
                    max_cell['sentences'].append(cur_cell) 
                    return_code = self.layering(max_cell, cur_cell, cur_size, cur_loc, current_page_cells)
                    
                    if return_code == -1:
                        break 
                
                self.CellList.append(max_cell)
    
                cell_text = self.TextList[0]
                current_page = cell_text.page_num
                max_size = cell_text.size
                max_y = cell_text.y0
                index = 0
                max_index = index
                
                
        if current_page:
            max_cell_text = current_page_cells.pop(max_index)
            max_cell = {'topic' : max_cell_text.text, 'keywords' : max_cell_text.keyword_set, 'page' : [max_cell_text.page_num],'sentences' : []}

            # layering 
            while current_page_cells:
                temp = current_page_cells.pop(0)
                cur_size = temp.size
                cur_loc = temp.x0
                cur_cell = {'text' : temp.text, 'keywords' : temp.keyword_set, 'sentences' : []}
                max_cell['sentences'].append(cur_cell) 
                return_code = self.layering(max_cell, cur_cell, cur_size, cur_loc, current_page_cells)
                
                if return_code == -1:
                    break 
            
            self.CellList.append(max_cell)
            
    
    ### RETURN CODE ###
    # -1 : empty list
    # 0 : terminate layering
    # 1 : return to caller 
    def layering(self, parent_cell, cur_cell, cur_size, cur_loc, page_cells):
        if len(page_cells) == 0:
            return -1

        temp = page_cells[0]
        if temp.symbol_start:
        # 형제로 
            if abs(temp.size - cur_size) < 0.1 and abs(temp.x0 - cur_loc) < temp.size/2:
                temp = page_cells.pop(0)
                temp_cell = {'text' : temp.text, 'keywords' : temp.keyword_set, 'sentences' : []}
                parent_cell['sentences'].append(temp_cell)
                return_code = self.layering(parent_cell, temp_cell, temp.size, temp.x0, page_cells)
                if return_code == 1:
                    return 1

            # 자식으로  
            elif (temp.size <= cur_size or abs(temp.size - cur_size) < 0.1) and temp.x0 > cur_loc:
                temp = page_cells.pop(0)
                temp_cell = {'text' : temp.text, 'keywords' : temp.keyword_set, 'sentences' : []}
                cur_cell['sentences'].append(temp_cell)
                return_code = self.layering(cur_cell, temp_cell, temp.size, temp.x0, page_cells)
                if return_code == 1:
                    if abs(page_cells[0].size - cur_size) < 1 and abs(page_cells[0].x0 - cur_loc) < 0.1:
                        temp = page_cells.pop(0)
                        temp_cell = {'text' : temp.text, 'keywords' : temp.keyword_set, 'sentences' : []}
                        parent_cell['sentences'].append(temp_cell)
                        return_code = self.layering(parent_cell, temp_cell, temp.size, temp.x0, page_cells)
                        if return_code == 1:
                            return 1
                                
                    elif page_cells[0].size >= cur_size and page_cells[0].x0 < cur_loc:
                        return 1 
                    else: 
                        return 0
                
            elif temp.size >= cur_size and temp.x0 < cur_loc:
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

    def is_special_symbol(self, input):
        if 48 <= ord(input) <= 57:              #digit 
            return 0  
        elif 65 <= ord(input) <= 90:            #eng
            return 1  
        elif 97 <= ord(input) <= 122:           #eng
            return 1  
        elif 44032 <= ord(input) <= 55215:      #kor 
            return 1  
        elif ord(input) == 32:
            return 2
        elif ord(input) == 34 or ord(input) == 39 or ord(input) == 8220:
            return 1
        else:
            return 3     
   
            
   
   
 