#!/usr/bin/env python
# -*- coding: utf-8 -*-

#function: 剪切更改图片尺寸大小
import os, argparse
import os.path
from fpdf import FPDF

def main():

	parser = argparse.ArgumentParser(description="Tool for pictures to pdf file")
	parser.add_argument('-f', '--fromdir', required=True, help='the directory path of the input file')
	parser.add_argument('-H', '--height',type=int, required=True, help='height of the output file')
	parser.add_argument('-W', '--width',type=int, required=True, help='width of the output file')
	parser.add_argument('-T', '--type', required=False, help='the type of the output file: jpeg, git, png ,etc')
	args = parser.parse_args()
	fromdir = args.fromdir
	width = args.width
	height = args.height
	if args.type == None:
		type = 'png'
	else:
		type = args.type
	pdf = FPDF( unit = 'pt')
	pdf.add_page()
	for file in range(3,126):
		file = "屏幕截图(" + str(file) + ").png"
		if file == "desktop.ini":
			continue
		filein = os.path.join(fromdir, file)
		print(filein)
		try:
			pdf.image(filein, None, None, width, height,"PNG")
		except Exception as e:
			print(e)
			continue
	pdf.output("yourfile.pdf", "F")
if __name__ == '__main__':
	main()