def detect_diff(self, chars, textline, index, page_num, default_color):
    # keyword checking stacks
    ColorDiffStack = SelectedStack()
    BoldDiffStack = SelectedStack()
    # text stack
    TextStack = []
    # keyword checking status
    ColorKeyword = False
    BoldKeyword = False

    current_color = default_color

    size = chars[index]['size']
    location = chars[index]['x0']
    keyword_set = set()
    box_num = textline['box number'] 

    for char_miner in textline['text']:
        if char_miner == chars[index]['text']:
            # COLOR
            # start keyword searching 
            if current_color != str(chars[index]['non_stroking_color']) and not ColorKeyword and not BoldKeyword:
                current_color = str(chars[index]['non_stroking_color'])
                ColorKeyword = True
                ColorDiffStack.push(char_miner)
                TextStack.extend(['<','k','s','>'])
            # continue keyword searching
            elif current_color == str(chars[index]['non_stroking_color']) and ColorKeyword:
                ColorDiffStack.push(char_miner)
            # stop keyword searching
            elif current_color != str(chars[index]['non_stroking_color']) and ColorKeyword:
                current_color = str(chars[index]['non_stroking_color'])
                ColorKeyword = False
                keyword_set.add(ColorDiffStack.pop_all())
                TextStack.extend(['<','k','e','>'])
            else:
                pass

            # FONT
            # start keyword searching 
            if 'Bold' in chars[index]['fontname'] and not BoldKeyword and not ColorKeyword:
                BoldKeyword = True
                BoldDiffStack.push(char_miner)
                TextStack.extend(['<','k','s','>'])
            # continue keyword searching
            elif 'Bold' in chars[index]['fontname'] and BoldKeyword:
                BoldDiffStack.push(char_miner)
            # stop keyword searching
            elif 'Bold' not in chars[index]['fontname'] and BoldKeyword:
                BoldKeyword = False
                keyword_set.add(BontDiffStack.pop_all())
                TextStack.extend(['<','k','e','>'])
            else:
                pass

            TextStack.append(char_miner)
            if index < len(chars)-1:
                index += 1

        else:
            if ColorKeyword:
                if char_miner == '\n':
                    current_color = default_color
                    ColorKeyword = False
                    keyword_set.add(ColorDiffStack.pop_all())
                    TextStack.extend(['<','k','e','>'])
                    
                elif char_miner == ' ':
                    ColorDiffStack.push(' ')
                    TextStack.append(' ')
                else:
                    raise Exception('mismatching detected!!')
                
            elif FontKeyword:
                if char_miner == '\n':
                    FontKeyword = False
                    keyword_set.add(BoldDiffStack.pop_all())
                    TextStack.extend(['<','k','e','>'])
            
                elif char_miner == ' ':
                    BoldDiffStack.push(' ')
                    TextStack.append(' ')
                else:
                    raise Exception('mismatching detected!!')
        
            else: 
                if char_miner == '\n' or char_miner == ' ':
                    TextStack.append(char_miner)
                    continue
                else:
                    raise Exception('mismatching detected!!')

    
    text = "".join(TextStack)
    self.TextListt.append(TextLine(text, size, location, keyword_set, page_num, box_num))
    return index

        