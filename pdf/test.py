from cgitb import text
from dataclasses import dataclass
import pdfplumber
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import *

def pick_default_color(chars):
    color_list = {}
    for char_plumber in chars:
        if char_plumber['stroking_color'] in color_list:
            color_list[char_plumber['stroking_color']] += 1
        else:
            color_list[char_plumber['stroking_color']] = 0
    
    return color_list
    # return max(color_list,key=color_list.get)
    
def pick_default_color2(chars):
    color_list2 = {}
    for char_plumber in chars:
        if str(char_plumber['non_stroking_color']) in color_list2:
            color_list2[str(char_plumber['non_stroking_color'])] += 1
        else:
            color_list2[str(char_plumber['non_stroking_color'])] = 0
    
    # return color_list2
    return max(color_list2,key=color_list2.get)

def pick_default_font(chars):
    font_list = {}
    for char_plumber in chars:
        if char_plumber['fontname'] in font_list:
            font_list[char_plumber['fontname']] += 1
        else:
            font_list[char_plumber['fontname']] = 0
    
    # return max(font_list,key=font_list.get)            
    return font_list        
            


with open('samples/mmm.pdf', 'rb') as input_file:
    with pdfplumber.PDF(input_file) as pdf_file:
        
        for page_miner, page_plumber in zip(extract_pages(input_file), pdf_file.pages):
            index = 0       # index for indicating character page_plumber``
            chars_plumber = page_plumber.chars
            
            if page_plumber.page_number == 2:
                for i in range(0,30):
                    print(chars_plumber[i]['non_stroking_color'])
                    print(chars_plumber[i]['fontname'])
                    print(chars_plumber[i]['text'])
                
                
                # for char_plumber in chars_plumber:
                #     print(char_plumber['stroking_color'])
                #     print(char_plumber['fontname'])
                #     print(char_plumber['text'])
                
                print(pick_default_color(chars_plumber))
                print(pick_default_color2(chars_plumber))
                print(pick_default_font(chars_plumber))
               
                
                


