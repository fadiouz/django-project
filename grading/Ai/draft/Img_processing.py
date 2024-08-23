from PIL import Image , ImageDraw

img = Image.open("test1.png")

print(img.format, img.size, img.mode)

#Draw line
draw = ImageDraw.Draw(img)

draw.line((0, img.size[1], img.size[0], 0), fill=(0,0,0) , width=2)
draw.ellipse((200, 125, 300, 200), fill=(255, 0, 0), outline=(0, 0, 0))

img.show()

