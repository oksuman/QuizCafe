class SelectedStack:
    def __init__(self):
        self.stack = []
    
    def push(self, input_char):
        # if 48 <= ord(input_char) <= 57:
        #     self.stack.append(input_char)   
        # elif 65 <= ord(input_char) <= 90:
        #     self.stack.append(input_char)   
        # elif 97 <= ord(input_char) <= 122:
        #     self.stack.append(input_char)   
        # elif 44032 <= ord(input_char) <= 55215:
        #     self.stack.append(input_char)  
        # elif ord(input_char) == 32:
        #     self.stack.append(input_char)
        # else:
        #     self.stack.append(' ')

        self.stack.append(input_char)
    def pop_all(self):
        char2string = ''.join(self.stack)
        # char2string = char2string.strip()
        self.stack.clear()
        return char2string
    
    def get_len(self):
        return len(self.stack)
        
        
    
        