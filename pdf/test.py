from dataclasses import dataclass 
#from typing import List
import pdfminer as pm
from pdfminer.high_level import extract_pages
from pdfminer.layout import * 

@dataclass
class TextLine:
    page_num : int
    size : int
    font : str
    text : str
    # position of the textline can be added

    def printLine(self):
        print("page : " + str(self.page_num))
        print("size : " + str(self.size))
        print("font : " + self.font)
        print("text : " + self.text)
        print()

        
TextList = []

page_num = 0
for page in extract_pages('samples/englishonly.pdf'):
    page_num += 1
    for element in page:
        if isinstance(element,LTTextBox):
            for textline in element:
                TextList.append(TextLine(page_num=page_num, size=list(textline)[0].size ,font=list(textline)[0].fontname ,text=repr(textline.get_text())))
                
for text in TextList:
   text.printLine()
