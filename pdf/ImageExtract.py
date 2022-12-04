import pdfplumber
import base64
count = 0

with open('QuizCafe/pdf/samples/chosun.pdf', 'rb') as input_file:
    with pdfplumber.PDF(input_file) as pdf_file:
        for page_plumber in pdf_file.pages:
            for image in page_plumber.images:
                count+= 1
                ph = page_plumber.height
                box = (image['x0'],ph - image['y1'], image['x1'], ph - image['y0'])
                size = int((image['x1'] -image['x0']) * (image['y1']- image['y0']))
                
                print(size)
                crop = page_plumber.crop(box)
                image_file = crop.to_image(resolution = 400)
                print(image_file)
                print(type(image_file))
                image_file.save('output' + str(count)+ '.png')         
                print('x0' + str(image['x0']))           
                print('x1' + str(image['x1']))           
                # print(image['x0'])
                # print(image['x1'])
                # print(image['y0'])
                # print(image['y1'])
print("사진 수 : " + str(count))
with open("output.png", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    print(str)        
                    