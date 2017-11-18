#!/usr/bin/env python
# -*- coding: utf-8 -*-

# function: 锐化图像
import os
import os.path
import sys
import getopt
import argparse
from PIL import Image, ImageEnhance


def sharpenPic(filein, fileout):

    im02 = Image.open(filein)

    im_30 = ImageEnhance.Sharpness(im02).enhance(2.0)

    im_30.save(fileout)


def main():
    parser = argparse.ArgumentParser(description="Tool for sharp the image")
    parser.add_argument('-f', '--fromdir', required=True, help='the directory path of the input file')
    parser.add_argument('-d', '--outdir', required=True, help='the directory of the output file')

    args = parser.parse_args()
    fromdir = args.fromdir
    outdir = args.outdir

    for file in os.listdir(fromdir):
        if file == "desktop.ini":
            continue
        filein = os.path.join(fromdir, file)
        fileout = os.path.join(outdir, file)
        try:
            sharpenPic(filein, fileout)
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    main()
