from dataclasses import dataclass


@dataclass
class TextLine:
    text: str
    size: float          
    # location
    x0: float
    x1: float
    y0: float
    keyword_set: list     # based on changes of color or size
    page_num: int        # page number that textline came from
    head_keyword: bool
    tail_keyword: bool
    symbol_start: bool


@dataclass
class Cell:
    text: str
    keywords: list
    subcells: list
