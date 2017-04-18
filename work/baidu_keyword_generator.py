#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import os
# import MySQLdb
import sys, getopt, argparse
import mysql.connector
import string
import encodings, codecs
import random
import json
from operator import itemgetter, attrgetter, methodcaller
import logging

reload(sys)
sys.setdefaultencoding('utf8')
from getSchoolProb import *

from EGKConfig import EGKConfig, eprint, EGK_GetLogger, EGK_GetDbConn, EGK_GetDbCursor
parser = argparse.ArgumentParser(description="Tool to get a list of possible schools given district/category/score based on detailed recruiting table.")
parser.add_argument('-v', '--verbose',  required=False, default=None, help="Message level. 10:'DEBUG'/20:'INFO'/30:'WARNING'/40:'ERROR'/50:'CRITICAL'")

parser.add_argument('--config', default='./egk.ini', help="the configuraiton file,db config")
args = parser.parse_args()
egkCfg = EGKConfig(args)
def get_baidu_keyword(curScore, district , category='理科'):
    curRank = getRankByScore(EGK_GetLogger(), EGK_GetDbConn(), EGK_GetDbCursor(), district, category,
                                 2016, curScore)
    tblName = District_PinYin_Map[district]
    adjLowBound = curRank
    if curRank < 5000:
        adjLowBound = 5000
    elif curRank < 55000:
        adjLowBound = 5000 + (curRank - 5000) / 3
    else:
        adjLowBound = 10000 + (curRank - 55000) / 10

    adjHighBound = 5000
    if curRank < 5000:
        pass
    elif curRank < 55000:
        adjHighBound = 5000 + (curRank - 5000) / 5
    else:
        adjHighBound = 10000 + (curRank - 55000) / 4


    sqlStr = "select * from rc_model \
            where (%d+%d>=highest_score_rank and %d<lowest_score_rank+%d) and %d+120 > average_score and %d < average_score+120\
            and district='%s' and category='%s' and year='%d' and round not like '%%提前%%' order by average_score asc limit %d" % (
            curRank, adjLowBound, curRank, adjHighBound, curScore, curScore, tblName, '理科', 2015, 550)
    EGK_GetLogger().debug("Query recruiting table - sql : %s" % (sqlStr))
    EGK_GetDbCursor().execute(sqlStr)

    schoolList = EGK_GetDbCursor().fetchall()
    if len(schoolList) == 0:
        EGK_GetLogger().error('{"ERROR":"No applicable school for score %d"}' % (curScore))
        sys.exit(-11)
    elif len(schoolList) > 10000:
        eprint('{"ERROR":"Too many school candiates for last year"}')
        sys.exit(-12)

    eprint("number of school list:%d Record #1:%s" % (len(schoolList), schoolList[0]))
    prevScore = -1
    curD = {}
    curD['district'] = district
    curD['year'] = 2016
    curD['category'] = '理科'
    curD['rank'] = curRank
    curD['prob'] = 0.0
    curD['prevScore'] = prevScore
    with open('baidu_keyword.csv', 'aw') as myfile:
        for k, v in enumerate(schoolList):
            curD['school'] = v['school_name'].encode('utf-8')
            getSchoolProb_V2_1(curD, v)
            if curD['prob'] >= 95.0:
                continue
            elif curD['prob'] >= 70.0:
                v['prob'] = 'medium'
            elif curD['prob'] >= 50.0:
                v['prob'] = 'low'
            else:
                v['prob'] = 'very_low'
            print('{} 分能考上{}吗'.format(curScore, ''.join(v['school_name'])), file=myfile)

if __name__ == '__main__':
    for district in ['河南', '北京']:
        for score in range(350,640,10):
            get_baidu_keyword(score,district,'理科')


# 统计各分数段可选学校多少
# cat baidu_keyword.csv|awk -F ' ' '{ua=$1 requests[ua]++} END{for(ua in requests){printf("%s\t%s\n",  requests[ua], ua)}}' | sort -nr | head -n 10
