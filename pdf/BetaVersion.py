  # Author : oksuman a.k.a. prince of kalbaram
# .pdf -> leveled string structure
# using pdfminer & pdfplumber

import pdfplumber
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import *
from SelectedStack import SelectedStack
from DataType import *
from Default import *
import json
    
# list of TextLine
TextList = []
combined_TextList = []
# list of Theme
ThemeList = []

MAX_COUNT = 100

def detect_diff(chars, textline, index, page_num, default_color, default_font):
    
    # keyword checking stacks
    # FontDiffStack = []
    ColorDiffStack = SelectedStack()
    # keyword checking status
    # FontKeyword = False
    ColorKeyword = False
    
    current_color = default_color
    # current_font = default_font

    temp = TextLine(textline['text'], chars[index]['size'], chars[index]['x0'], [], page_num, textline['box number'])
    keyword_set = set() 

    for char_miner in textline['text']:
        if char_miner == chars[index]['text']:
            # COLOR 
            # start keyword searching 
            if current_color != str(chars[index]['non_stroking_color']) and ColorKeyword == False:
                current_color = str(chars[index]['non_stroking_color'])
                ColorKeyword = True
                ColorDiffStack.push(char_miner)
            # continue keyword searching
            elif current_color == str(chars[index]['non_stroking_color']) and ColorKeyword == True:
                ColorDiffStack.push(char_miner)
            # stop keyword searching
            elif current_color != str(chars[index]['non_stroking_color']) and ColorKeyword == True:
                current_color = str(chars[index]['non_stroking_color'])
                ColorKeyword = False
                keyword_set.add(ColorDiffStack.pop_all())
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
                    keyword_set.add(ColorDiffStack.pop_all())
                      
                elif char_miner == ' ':
                    ColorDiffStack.push(' ')
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
 
def combine(TextList):
    
    combined_textline = TextList.pop(0)
    current_page = combined_textline.page_num
    current_box = combined_textline.box_num

    combined_text = []
    combined_text.append(combined_textline.text.strip())
    while TextList:
        if TextList[0].page_num == current_page and TextList[0].box_num == current_box:
            temp = TextList.pop(0)  
            combined_text.append(temp.text.strip())
            combined_textline.keyword_set.update(temp.keyword_set)

        else:
            combined_textline.text = "".join(combined_text)
            combined_TextList.append(combined_textline)

            combined_textline = TextList.pop(0)
            current_page = combined_textline.page_num
            current_box = combined_textline.box_num
            
            combined_text.clear()
            combined_text.append(combined_textline.text.strip())

    return combined_TextList

# Korean Traditional Folk Game
def Tuho(TextList):
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
             
            theme.arrows.add(arrow(textline.text, textline.keyword_set))
            if TextList: 
                next_page_num = TextList[0].page_num
            else:
                break
        
        is_present_quiver = False
        if ThemeList:
            for set_theme in ThemeList:
                if set_theme.quiver == theme.quiver:
                    is_present_quiver = True
                    set_theme.arrows.array.extend(theme.arrows.array)
                    
            if is_present_quiver:
                pass
            else:
                ThemeList.append(theme)

        else:
            ThemeList.append(theme)   
        
 
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
            pending_count = 0

            box_num = 0
            for element in page_miner:
                if isinstance(element, LTTextBox):
                    for textline in element:
                        if isinstance(textline, LTTextLine):
                            textlines.append({'text' : textline.get_text(), 'box number' : box_num})
                    box_num += 1
                            
            while textlines or pending_list:
                if textlines:
                    textline = textlines.pop(0)
                else:
                    textline = pending_list.pop(0)
                    pending_count += 1

                if textline['text'][0] == chars_plumber[index]['text']:
                    try:
                        index = detect_diff(chars_plumber, textline, index, page_number, page_default_color, page_default_font)
                    except: 
                        pending_list.append(textline)
                        continue
        
                else:
                    pending_list.append(textline) 
                    for pending_index in range(len(pending_list)):
                        if pending_list[pending_index]['text'][0] == chars_plumber[index]['text']:    
                            pending_textline = pending_list.pop(pending_index)
                            try:
                                index = detect_diff(chars_plumber, pending_textline, index, page_number, page_default_color, page_default_font)
                            except:
                                pending_list.append(pending_textline)  
                            break       
                        else:
                            continue    

                if pending_count > MAX_COUNT:
                    break
                            
            if pending_list:
                pending_list.clear()
                print('pdf extracion is not perfect !!')

 
combine(TextList)
Tuho(combined_TextList)   


# with open('output.json', 'w', encoding="utf-8") as output:
#     json.dump(ThemeList, output, ensure_ascii=False, indent='\t')

# with open("output.txt","w") as output:
#     for textline in combined_TextList:
#         output.write(repr(textline.text))
#         output.write("  ")
#         output.write(str(textline.keyword_set))
#         output.write("  ")
#         output.write(str(textline.size))
#         output.write("  ")
#         output.write(str(textline.location))
#         output.write("  ")
#         output.write(str(textline.page_num))
#         output.write("\n")
        
# Tuho(combined_TextList)                    
                                                
with open("outputput.txt","w") as output2:
    num = 1
    for theme in ThemeList:
        output2.write("\n")
        output2.write("주제 " + str(num) + " : " + theme.quiver)
        for arrow in theme.arrows.array:
            output2.write("\n")
            output2.write("문장 : " + arrow.text)
            output2.write("\n")
            output2.write("키워드 : ")
            for keyword in arrow.keyword_set:
                output2.write(keyword)
                output2.write(" ")
            output2.write('\n')
        output2.write('\n')
        num += 1
                
            
     
