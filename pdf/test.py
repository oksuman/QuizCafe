from SelectedStack import SelectedStack 

stack = SelectedStack()

array = ['a',' ', '가',')','-','닯',';','!','n',' ']


for element in array:
    stack.push(element)



print(stack.stack)    
str = stack.pop_all()
print(str)

print(stack.stack) 

str = ""

if str:
    print("진실")
else:
    print("거짓")