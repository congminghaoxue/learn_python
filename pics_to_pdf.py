#!/usr/bin/env python
# -*- coding: utf-8 -*-

# function: 剪切更改图片尺寸大小
import os
import argparse
import os.path
from fpdf import FPDF


class PDF(FPDF):

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, "Suooter内部使用，禁止传播", 0, 0, 'C')


def main():
    parser = argparse.ArgumentParser(description="Tool for pictures to pdf file")
    parser.add_argument('-f', '--fromdir', required=True, help='the directory path of the input file')
    parser.add_argument('-H', '--height', type=int, required=True, help='height of the output file')
    parser.add_argument('-W', '--width', type=int, required=True, help='width of the output file')
    args = parser.parse_args()
    fromdir = args.fromdir
    width = args.width
    height = args.height

    pdf = FPDF(unit='pt')
    pdf.footer()
    pdf.add_page()
    for file in range(3, 126):
        file = "屏幕截图(" + str(file) + ").png"
        if file == "desktop.ini":
            continue
        filein = os.path.join(fromdir, file)
        print(filein)
        try:
            pdf.image(filein, None, None, width, height, "PNG")
        except Exception as e:
            print(e)
            continue
    pdf.output("yourfile.pdf", "F")


if __name__ == '__main__':
    main()
