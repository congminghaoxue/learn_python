#!/usr/bin/env python
# encoding: utf-8

import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
pdfmetrics.registerFont(TTFont('song', '/Library/Fonts/Microsoft/Kaiti.ttf'))
pdfmetrics.registerFont(TTFont('hei', '/Library/Fonts/Microsoft/Kaiti.ttf'))

from reportlab.lib import fonts
fonts.addMapping('song', 0, 0, 'song')
fonts.addMapping('song', 0, 1, 'song')
fonts.addMapping('song', 1, 0, 'hei')
fonts.addMapping('song', 1, 1, 'hei')

import copy
t = '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <!--兼容低版本的IE   IE-edge--> <link rel="icon" type="image/png" sizes="32x32" href="favicon.png"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="version" content="8124d0dae6778594340ab135e0ba4b4279d42a76"> <meta name="viewport"content="width=device-width,initial-scale=1.0,minimum-scale=0.5,maximum-scale=1.0,user-scalable=no"> <title>网站正在建设中，请稍候访问！</title> </head> <style> body {margin: 0; padding: 0; font-size: 12px; } #main {width: 70%; margin: 20px auto; padding: 10px; border: 10px solid #F2F8FF; vertical-align: middle; } #pic {margin: 20px auto; padding-bottom: 10px; text-align: center; } #content {margin: 20px auto; text-align: center; } #contentDetail {width: 90%; margin: 10px auto; word-wrap: break-word; word-break: normal; } </style> <meta name="chromesniffer" id="chromesniffer_meta" content="{}"><script type="text/javascript" src="chrome-extension://fhhdlnnepfjhlhilgmeepgkhjmhhhjkh/js/detector.js"></script></head> <body> <div id="main"> <div id="pic"><img id="errorImage" src="img/house.gif"></div> <div id="content"><h1>网站正在建设中，请稍候访问！<span style="color: #E0F0FF;"></span></h1></div> <div id="contentDetail"></div> </div> </body> </html>'
from reportlab.platypus import Paragraph, SimpleDocTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
stylesheet=getSampleStyleSheet()
normalStyle = copy.deepcopy(stylesheet['Normal'])
normalStyle.fontName ='song'
normalStyle.fontSize = 20
story = []
story.append(Paragraph(t, normalStyle))
doc = SimpleDocTemplate('hello.pdf')
doc.build(story)
