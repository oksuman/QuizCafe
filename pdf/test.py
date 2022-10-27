import string
from typing import final
import pdfplumber
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import *
from SelectedStack import SelectedStack
from DataType import *
from Default import *
import json


with open('samples/ssogong.pdf', 'rb') as input_file:
    with pdfplumber.PDF(input_file) as pdf_file:
        for page_miner, page_plumber in zip(extract_pages(input_file), pdf_file.pages):
        
            for element in page_miner:
                if page_plumber.page_number == 8:
                    count = 0
                    for char in page_plumber.chars:
                        if 'Bold' in char['fontname']:
                            print(char['text'])
                            print(char['fontname'])
                            print(char['non_stroking_color'])
                            count += 1
                    
                    # if isinstance(element, LTTextBox):
                    #     for textline in element:
                    #         if isinstance(textline, LTTextLine):
                    #             print(textline.get_text())