from django.test import TestCase

from PIL import Image,ImageFont,ImageDraw
text = u'欢迎访问脚本之家,http://www.jb51.net'
font = ImageFont.truetype("msyh.ttf",18)
lines = []
line =''
for word in text.split():
  print word
  if font.getsize(line+word)[0] >= 300:
    lines.append(line)
    line = u''
    line += word
    print 'size=',font.getsize(line+word)[0]
  else:
    line = line + word
line_height = font.getsize(text)[1]
img_height = line_height*(len(lines)+1)
print 'len=',len(lines)
print 'lines=',lines
im = Image.new("RGB",(444,img_height),(255,255,255))
dr = ImageDraw.Draw(im)
x,y=5,5
for line in lines:
  dr.text((x,y),line,font=font,fill="#000000")
  y += line_height

im.save("1.1.jpg")
