from PIL import Image , ImageDraw
import cv2

img = Image.open("Data/paper2 section.jpg")

# Load the image
# image = cv2.imread('../Data Set/paper section.jpg')


print(img.format, img.size, img.mode)

# Draw line
draw = ImageDraw.Draw(img)

# i=0
# step = img.size[1]/25
# while i < img.size[1]:
#     count = int(i)
#     draw.line((0, count, img.size[0], count), fill=(0,0,0) , width=2)
#     i+=step

# for i  in range(0 , img.size[1], int(img.size[1]/12)):
#     draw.line((0, i, img.size[0], i), fill=(0,0,0) , width=2)

draw.line((0, int(img.size[1]/2), img.size[0], int(img.size[1]/2)), fill=(0,0,0) , width=2)


img.show()