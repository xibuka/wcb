#!/usr/bin/python 
# -*- coding: utf-8 -*-

from PIL import Image
import sys, os
import argparse

#命令行输入参数处理
parser = argparse.ArgumentParser()

parser.add_argument('file')     #输入文件
parser.add_argument('-o', '--output')   #输出文件
parser.add_argument('--width', type = int, default = 160) #输出字符画宽
parser.add_argument('--height', type = int, default = 160) #输出字符画高

#获取参数
args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
#ascii_char = list(r"$@&%B#=-. ")


def sketch(img, threshold):
    '''
    素描
    param img: Image实例
    param threshold: 介于0到100
    '''
    if threshold < 0: threshold = 0
    if threshold > 100: threshold = 100
     
    width, height = img.size
    img = img.convert('L') # convert to grayscale mode
    pix = img.load() # get pixel matrix
 
    for w in xrange(width):
        for h in xrange(height):
            if w == width-1 or h == height-1:
                continue
             
            src = pix[w, h]
            dst = pix[w+1, h+1]
 
            diff = abs(src - dst)
 
            if diff >= threshold:
                pix[w, h] = 0
            else:
                pix[w, h] = 255
 
    return img

# 将256灰度映射到70个字符上
def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]

# 把RGB转为灰度值，并且返回该灰度值对应的字符标记
def select_ascii_char(r, g, b, alpha = 256):
    if alpha == 0:
        return ' '
    gray = int((19595 * r + 38469 * g + 7472 * b) >> 16)  # ‘RGB－灰度值’转换公式
    unit = 256.0/len(ascii_char)  # ascii_char中的一个字符所能表示的灰度值区间
    return ascii_char[int(gray/unit)]

if __name__ == '__main__':

    im = Image.open(IMG)
    im = im.resize((WIDTH,HEIGHT), Image.NEAREST)
    rgb_im = im.convert('RGBA')

    txt = ""

    for i in range(HEIGHT):
        for j in range(WIDTH):
             r,g,b,alpha = rgb_im.getpixel((j,i))
             #txt += get_char(r,g,b,alpha)
             txt += select_ascii_char(r,g,b,alpha)
        txt += '\n'

    # print(txt)

    #字符画输出到文件
    if OUTPUT:
        with open(OUTPUT,'w') as f:
            f.write(txt)
    else:
        with open("output.txt",'w') as f:
            f.write(txt)

    threshold = 15
    sketch_img = sketch(im, threshold)
    sketch_img.save(IMG + '.sketch.jpg', 'JPEG')
