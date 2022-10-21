# Author : oksuman a.k.a. prince of kalbaram
# .pdf -> leveled string structure
# using pdfminer & pdfplumber

from dataclasses import dataclass
import pdfplumber
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import *

@dataclass
class TextLine:
    text: str
    size: int            
    location: float       # point where textline starts
    keyword_set: list     # based on changes of color or size
    page_num : int        # page number that textline came from 

# list of TextLine
TextList = []

def pick_default_stroking_color(chars):
    stroking_color_list = {}
    for char_plumber in chars:
        if char_plumber['stroking_color'] in stroking_color_list:
            stroking_color_list[char_plumber['stroking_color']] += 1
        else:
            stroking_color_list[char_plumber['stroking_color']] = 0
    
    return max(stroking_color_list,key=stroking_color_list.get)

def pick_default_color(chars):
    color_list = {}
    for char_plumber in chars:
        if str(char_plumber['non_stroking_color']) in color_list:
            color_list[str(char_plumber['non_stroking_color'])] += 1
        else:
            color_list[str(char_plumber['non_stroking_color'])] = 0
 
    return max(color_list,key=color_list.get)

def pick_default_font(chars):
    font_list = {}
    for char_plumber in chars:
        if char_plumber['stroking_color'] in font_list:
            font_list[char_plumber['fontname']] += 1
        else:
            font_list[char_plumber['fontname']] = 0
    
    return max(font_list,key=font_list.get)


def detect_diff(chars, textline, index, page_num, default_color, default_font):
    
    # keyword checking stacks
    # FontDiffStack = []
    ColorDiffStack = []
    # keyword checking status
    # FontKeyword = False
    ColorKeyword = False
    
    current_color = default_color
    # current_font = default_font

    temp = TextLine(textline, chars[index]['size'], chars[index]['x0'], [], page_num)
    keyword_set = [] 

    for char_miner in textline:
        if char_miner == chars[index]['text']:
            # COLOR 
            # start keyword searching 
            if current_color != str(chars[index]['non_stroking_color']) and ColorKeyword == False:
                current_color = str(chars[index]['non_stroking_color'])
                ColorKeyword = True
                ColorDiffStack.append(char_miner)
            # continue keyword searching
            elif current_color == str(chars[index]['non_stroking_color']) and ColorKeyword == True:
                ColorDiffStack.append(char_miner)
            # stop keyword searching
            elif current_color != str(chars[index]['non_stroking_color']) and ColorKeyword == True:
                current_color = str(chars[index]['non_stroking_color'])
                ColorKeyword = False
                keyword_set.append(''.join(ColorDiffStack))
                ColorDiffStack.clear()
            else:
                pass
                        
            # FONT
            # # start keyword searching 
            # if current_font != chars[index]['fontname'] and FontKeyword == False:
            #     current_font = chars[index]['fontname']
            #     FontKeyword = True
            #     FontDiffStack.append(char_miner)
            # # continue keyword searching
            # elif current_font == chars[index]['fontname'] and FontKeyword == True:
            #     FontDiffStack.append(char_miner)
            # # stop keyword searching
            # elif current_font != chars[index]['fontname'] and FontKeyword == True:
            #     current_font = chars[index]['fontname']
            #     FontKeyword = False
            #     keyword_set.append(''.join(FontDiffStack))
            #     FontDiffStack.clear()
            # else:
            #     pass
            
            if index < len(chars) -1:
                index += 1
           
        
        # 글자가 달라. 개행문자 처리. ' '는 계속 탐색하고 '\n'는 멈추자
        else:
            # if ColorKeyword and FontKeyword:
            #     if char_miner == '\n':
            #         current_color = default_color
            #         ColorKeyword = False
            #         keyword_set.append(''.join(ColorDiffStack))
            #         ColorDiffStack.clear()  
                    
            #         current_font = default_font
            #         FontKeyword = False
            #         keyword_set.append(''.join(FontDiffStack))
            #         FontDiffStack.clear()  
            #     elif char_miner == ' ':
            #         ColorDiffStack.append(' ')
            #         FontDiffStack.append(' ')
            #     else:
            #         raise Exception('mismatching detected!!')
            if ColorKeyword:
                if char_miner == '\n':
                    current_color = default_color
                    ColorKeyword = False
                    keyword_set.append(''.join(ColorDiffStack))
                    ColorDiffStack.clear()  
                elif char_miner == ' ':
                    ColorDiffStack.append(' ')
                else:
                    raise Exception('mismatching detected!!')
                    
            # elif FontKeyword:
            #     if char_miner == '\n':
            #         current_font = default_font
            #         FontKeyword = False
            #         keyword_set.append(''.join(FontDiffStack))
            #         FontDiffStack.clear()  
            #     elif char_miner == ' ':
            #         FontDiffStack.append(' ')
            #     else:
            #         raise Exception('mismatching detected!!')
            else: 
                if char_miner == '\n' or char_miner == ' ':
                    continue
                else:
                    raise Exception('mismatching detected!!')
            
    temp.keyword_set = keyword_set
    TextList.append(temp)
    
    return index 
 
 
with open('pdf/samples/mmm.pdf', 'rb') as input_file:
    with pdfplumber.PDF(input_file) as pdf_file:
        for page_miner, page_plumber in zip(extract_pages(input_file), pdf_file.pages):
            
            chars_plumber = page_plumber.chars
            index = 0       # index for indicating character page_plumber
            page_default_color = pick_default_color(chars_plumber)
            page_default_font = pick_default_font(chars_plumber)
            page_number = page_plumber.page_number
            
            textlines = []
            # list of pending_textline
            # for unmatched textline between pdfminer and pdfplumber
            pending_list = []
            
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

                if textline[0] == chars_plumber[index]['text']:
                    try:
                        index = detect_diff(chars_plumber, textline, index, page_number, page_default_color, page_default_font)
                    except: 
                        pending_list.append(textline)
                        continue
        
                else:
                    pending_list.append(textline) 
                    for pending_index in range(len(pending_list)):
                        if pending_list[pending_index][0] == chars_plumber[index]['text']:    
                            pending_textline = pending_list.pop(pending_index)
                            try:
                                index = detect_diff(chars_plumber, pending_textline, index, page_number, page_default_color, page_default_font)
                            except:
                                pending_list.append(pending_textline)  
                            break       
                        else:
                            continue    
                                
            # 한 페이지 다 읽었는데 pending list 남아있다면 예외 발생
            # if pending_list:
            #     print(page_number)
            #     print(pending_list)
            #     raise Exception('pendig list is not empty!!')
                    
                                                
# Korean Traditional Folk Game
def Tuho(TextList):
    pass
    
    
with open("output.txt","w") as output:
    for textline in TextList:
        output.write(repr(textline.text))
        output.write("  ")
        output.write(str(textline.keyword_set))
        output.write("  ")
        output.write(str(textline.size))
        output.write("  ")
        output.write(str(textline.location))
        output.write("  ")
        output.write(str(textline.page_num))
        output.write("\n")
        
