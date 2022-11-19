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

with open('QuizCafe/pdf/samples/ssogong.pdf', 'rb') as input_file:
    with pdfplumber.PDF(input_file) as pdf_file:
        for page_miner, page_plumber in zip(extract_pages(input_file), pdf_file.pages):
            
            if page_plumber.page_number == 3:
                for char in page_plumber.chars:
                    print(char['text'] +' '+ str(char['size']) + ' ' + str(char['x0']))
            
            
            # chars_plumber = page_plumber.chars
            # index = 0                       # index for indicating character page_plumber
            # page_default_color = pick_default_color(chars_plumber)
            # page_number = page_plumber.page_number
            
            # textlines = []
            # pending_list = []
            # # list of pending_textline
            # # for unmatched textline between pdfminer and pdfplumber
            # pending_count = 0 

            # for element in page_miner:
            #     if isinstance(element, LTTextBox):
            #         for textline in element:
            #             if isinstance(textline, LTTextLine):
            #                 textlines.append(textline.get_text())