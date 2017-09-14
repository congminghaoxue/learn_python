#!/usr/bin/env python
# -*- coding: utf-8 -*-

#function: 剪切更改图片尺寸大小
import os
import os.path
import sys, getopt, argparse
from PIL import Image

from change_pic_size_by_cut import CutImage

def main():
	argc = len(sys.argv)
	cmdargs = str(sys.argv)
	parser = argparse.ArgumentParser(description="Tool for batch cut the image")
	parser.add_argument('-f', '--fromdir', required=True, help='the directory path of the input file')
	parser.add_argument('-H', '--height',type=int, required=True, help='height of the output file')
	parser.add_argument('-W', '--width',type=int, required=True, help='width of the output file')
	parser.add_argument('-d', '--outdir', required=True, help='the directory of the output file')
	parser.add_argument('-T', '--type', required=False, help='the type of the output file: jpeg, git, png ,etc')
	args = parser.parse_args()
	fromdir = args.fromdir
	outdir = args.outdir
	width = args.width
	height = args.height
	if args.type == None:
		type = 'png'
	else:
		type = args.type
	for file in os.listdir(fromdir):
		if file == "desktop.ini":
			continue
		filein = os.path.join(fromdir, file)
		fileout = os.path.join(outdir, file)
		try:
			CutImage(filein, fileout, width, height, type)
		except Exception as e:
			print(e)
			continue
if __name__ == '__main__':
	main()