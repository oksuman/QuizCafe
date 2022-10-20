# Author : oksuman a.k.a. prince of kalbaram
# .pdf -> leveled string structure
# using pdfminer & pdfplumber

from dataclasses import dataclass
import pdfplumber
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import *

MAX_COUNT = 5 

@dataclass
class TextLine:
    text: str
    size: int            
    location: float       # point where textline starts
    keyword_set: list     # based on changes of color or size
    page_num : int        # page number that textline came from 
    parent: str           # reference by shallow copy
    level: int
    


# list of TextLine
TextList = []

# keyword checking stacks
FontDiffStack = []
ColorDiffStack = []
# keyword checking status
FontKeyword = False
ColorKeyword = False


with open('samples/comtong.pdf', 'rb') as input_file:
    with pdfplumber.PDF(input_file) as pdf_file:
        for page_miner, page_plumber in zip(extract_pages(input_file), pdf_file.pages):
            index = 0       # index for indicating character page_plumber
            chars_plumber = page_plumber.chars
            pending_textline = []

            for element in page_miner:
                if isinstance(element, LTTextBox):
                    for textline in element:
                        if isinstance(textline, LTTextLine):
                            # switching process
                            # plumber에서 추출한 글자에 맞춰, 일치하는 miner의 textline을 찾을 때까지 반복
                            # reject된 miner의 textline은 pending_textline 에서 대기
                            if textline.get_text()[0] != chars_plumber[index]['text']: #or list(textline)[0].size != chars_plumber[index]['size'] or list(textline)[0].fontname != chars_plumber[index]['fontname']:
                                pending_textline.append(textline)
                                break

                            # after swithcing process
                            # plumber와 miner가 읽고있는 textline이 일치
                            # 현재 읽고 있는 textline에 대해 TextLine 객체를 생성한다
                            temp_text = textline.get_text()
                            temp_size = chars_plumber[index]['size']
                            temp_location = chars_plumber[index]['x0']
                            temp_keyword_set = []

                            current_color = 0
                            for char_miner in textline.get_text():
                                # 두 모듈이 식별한 글자가 같은 경우
                                if char_miner == chars_plumber[index]['text']:
                                    # start keyword searching
                                    if current_color != chars_plumber[index]['stroking_color'] and ColorKeyword == False:
                                        current_color = chars_plumber[index]['stroking_color']
                                        ColorKeyword = True
                                        ColorDiffStack.append(char_miner)

                                    # continue keyword searching
                                    elif current_color == chars_plumber[index]['stroking_color'] and ColorKeyword == True:
                                        ColorDiffStack.append(char_miner)

                                    # stop keyword searching
                                    elif current_color != chars_plumber[index]['stroking_color'] and ColorKeyword == True:
                                        current_color = chars_plumber[index]['stroking_color']
                                        ColorKeyword = False
                                        temp_keyword_set.append(''.join(ColorDiffStack))
                                        ColorDiffStack.clear()

                                    else:
                                        pass
                                    if (index < len(chars_plumber)-1):
                                        index += 1

                                # 두 모듈이 식별한 글자가 다른 경우
                                # 키워드 탐색 중 만난 개행문자 및 띄어쓰기에 대한 처리
                                else:
                                    if ColorKeyword:
                                        if char_miner == '\n':
                                            current_color = 0
                                            ColorKeyword = False
                                            temp_keyword_set.append(''.join(ColorDiffStack))
                                            ColorDiffStack.clear()
                                            continue
                                        elif char_miner == ' ':
                                            ColorDiffStack.append(' ')
                                            continue
                                        else:
                                            continue
                                    else:
                                        continue
                            TextList.append(TextLine(temp_text, temp_size, temp_location, temp_keyword_set, page_plumber.page_number, "none", 0))
                        else: 
                            continue            

            # end reading a page 
            # solving pending textlines!!
            pending_count = 0
            while pending_textline and pending_count < MAX_COUNT:
                temp = pending_textline.pop(0)
                if temp.get_text()[0] == chars_plumber[index]['text']:
                    temp_text = temp.get_text()
                    temp_size = chars_plumber[index]['size']
                    temp_location = chars_plumber[index]['x0']
                    temp_keyword_set = []

                    current_color = 0
                    for char_miner in temp.get_text():
                        # 두 모듈이 식별한 글자가 같은 경우
                        if char_miner == chars_plumber[index]['text']:
                            if current_color != chars_plumber[index]['stroking_color'] and ColorKeyword == False:  # start keyword searching 
                                current_color = chars_plumber[index]['stroking_color']
                                ColorKeyword = True
                                ColorDiffStack.append(char_miner)

                            elif current_color == chars_plumber[index]['stroking_color'] and ColorKeyword == True:  # continue keyword searching
                                ColorDiffStack.append(char_miner)

                            elif current_color != chars_plumber[index]['stroking_color'] and ColorKeyword == True:  # stop keyword searching
                                current_color = chars_plumber[index]['stroking_color']
                                ColorKeyword = False
                                temp_keyword_set.append(''.join(ColorDiffStack))
                                ColorDiffStack.clear()

                            else:
                                pass
                            if (index < len(chars_plumber)-1):
                                index += 1

                        else:
                            if ColorKeyword:
                                if char_miner == '\n':
                                    current_color = 0
                                    ColorKeyword = False
                                    temp_keyword_set.append(''.join(ColorDiffStack))
                                    ColorDiffStack.clear()
                                    continue
                                elif char_miner == ' ':
                                    ColorDiffStack.append(' ')
                                    continue
                                else:
                                    continue
                            else:
                                continue

                    current_line = TextLine(temp_text, temp_size,temp_location,temp_keyword_set, page_plumber.page_number, "none", 0)
                    TextList.append(current_line)

                else:
                    pending_textline.append(temp)
                    pending_count += 1
                    continue
                
        for textline in TextList:
            print(repr(textline.text))
            print(textline.keyword_set)
            print(textline.size)
            print(textline.location)
            print(textline.page_num)
            print()
      



