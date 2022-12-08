class SelectedStack:
    def __init__(self):
        self.stack = []
    
    def push(self, input_char):
        self.stack.append(input_char)
        
    def pop_all(self):
        char2string = ''.join(self.stack)
        self.stack.clear()
        return char2string
    
    def get_len(self):
        return len(self.stack)
