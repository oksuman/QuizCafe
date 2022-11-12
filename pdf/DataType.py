from dataclasses import dataclass

<<<<<<< HEAD
=======

>>>>>>> backend
@dataclass
class TextLine:
    text: str
    size: int            
    location: float       # point where textline starts
    keyword_set: set      # based on changes of color or size
<<<<<<< HEAD
    page_num : int        # page number that textline came from 
    box_num : int
=======
    page_num: int        # page number that textline came from
    box_num: int
>>>>>>> backend


@dataclass
class Theme:
    quiver: str
    arrows: list          # arrows : list of arrow
<<<<<<< HEAD
    
@dataclass
class arrow:
    text: str
    keyword_set: set
    
=======


@dataclass
class Arrow:
    text: str
    keyword_set: set


>>>>>>> backend
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
<<<<<<< HEAD
    
=======
>>>>>>> backend
