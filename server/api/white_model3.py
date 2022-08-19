from PIL import Image

def white_image(object_name):
    print(object_name)
    image = Image.open('./code/code/C-SPADE/datasets/RGB/'+object_name+'_0.png')
    image = image.convert('RGBA')
    print(image.mode)


    # Transparency
    newImage = []
    for item in image.getdata():
        if item[:3] == (0, 0, 0):
            newImage.append((255, 255, 255, 0))
        else:
            newImage.append(item)

    image.putdata(newImage)


    image.save('./white_pictures/'+object_name+'_0.png')
    print(image.mode, image.size)
