from dataclasses import dataclass

@dataclass
class TextLine:
    text: str
    size: float          
    location: float         # point where textline starts
    keyword_set: list     # based on changes of color or size
    page_num : int        # page number that textline came from 

    
@dataclass
class Cell:
    text : str
    keywords : list
    subcells : list 

