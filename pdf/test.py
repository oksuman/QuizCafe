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


with open('pdf/samples/mmm.pdf', 'rb') as input_file:
    with pdfplumber.PDF(input_file) as pdf_file:
        for page_miner, page_plumber in zip(extract_pages(input_file), pdf_file.pages):
        
            for element in page_miner:
                if isinstance(element, LTTextBox):
                    print("new box")
                    for textline in element:
                        if isinstance(textline, LTTextLine):
                            print(textline.get_text())