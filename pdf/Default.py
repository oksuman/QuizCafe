def pick_default_stroking_color(chars):
    stroking_color_list = {}
    for char_plumber in chars:
        if char_plumber['stroking_color'] in stroking_color_list:
            stroking_color_list[char_plumber['stroking_color']] += 1
        else:
            stroking_color_list[char_plumber['stroking_color']] = 0
    
    return max(stroking_color_list,key=stroking_color_list.get)

def pick_default_color(chars):
    color_list = {}
    for char_plumber in chars:
        if str(char_plumber['non_stroking_color']) in color_list:
            color_list[str(char_plumber['non_stroking_color'])] += 1
        else:
            color_list[str(char_plumber['non_stroking_color'])] = 0
 
    return max(color_list,key=color_list.get)

def pick_default_font(chars):
    font_list = {}
    for char_plumber in chars:
        if char_plumber['fontname'] in font_list:
            font_list[char_plumber['fontname']] += 1
        else:
            font_list[char_plumber['fontname']] = 0
    
    return max(font_list,key=font_list.get)
