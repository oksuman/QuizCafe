from dataclasses import dataclass

@dataclass
class TextLine:
    text: str
    size: int            
    location: int         # point where textline starts
    keyword_set: list     # based on changes of color or size
    page_num : int        # page number that textline came from 

    
@dataclass
class Cell:
    text : str
    keywords : list
    subcells : list 

    

@dataclass
class Theme:
    quiver: str
    arrows: list          # arrows : list of arrow
    
@dataclass
class Arrow:
    text: str
    keyword_set: list
    
class Arrows:
    def __init__(self):
        self.array = []
        
    def add(self, input_arrow):
        is_in_array = False
        if self.array:
            for arrow in self.array:
                if arrow.text == input_arrow.text:
                    is_in_array = True
                    break
                else:
                    continue
            if is_in_array:
                pass
            else:
                self.array.append(input_arrow)   
        else:
            self.array.append(input_arrow)