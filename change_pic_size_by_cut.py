#!/usr/bin/env python
# -*- coding: utf-8 -*-

# function: 剪切更改图片尺寸大小
import os
import os.path
import sys
import argparse
from PIL import Image


def CutImage(filein, fileout, width, height, type):
    '''
    # 从左上角开始 剪切 width*height的图片
    filein:  输入图片
    fileout: 输出图片
    width: 输出图片宽度
    height:输出图片高度
    type:输出图片类型（png, gif, jpeg...）
    '''
    img = Image.open(filein)
    out = img.crop((1, 1, width, height))
    out.save(fileout, type)


if __name__ == "__main__":
    argc = len(sys.argv)
    cmdargs = str(sys.argv)
    parser = argparse.ArgumentParser(description="Tool to get schools given district/category/score")
    parser.add_argument('-f', '--file', required=True, help='the file path of the input file')
    parser.add_argument('-H', '--height', type=int, required=True, help='height of the output file')
    parser.add_argument('-W', '--width', type=int, required=True, help='width of the output file')
    parser.add_argument('-T', '--type', required=False, help='the type of the output file: jpeg, git, png ,etc')
    args = parser.parse_args()
    filein = args.file
    width = args.width
    height = args.height
    f, e = os.path.splitext(filein)
    if args.type is None:
        type = 'png'
    else:
        type = args.type
    fileout = f + "_" + str(width) + "_" + str(height) + '.' + type
    CutImage(filein, fileout, width, height, type)
