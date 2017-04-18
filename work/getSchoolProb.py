#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: getSchoolProb.py
#
# This file implements a function to caclculate the admission probability for a student to be enrolled into a school.
# Algorithm details to be filled  later.

from __future__ import print_function
import os
#import MySQLdb
import sys, getopt, argparse
import mysql.connector
import string
import encodings,codecs
import random
from operator import itemgetter,attrgetter,methodcaller
import logging
import ast

from EGKConfig import EGKConfig,eprint,EGK_GetLogger,EGK_GetDbConn,EGK_GetDbCursor

DistrictList =  ['上海','云南','内蒙古','北京','吉林','四川','天津','宁夏','安徽','山东','山西','广东','广西','新疆','江苏',
        '江西','河北','河南','浙江','海南','湖北','湖南','甘肃','福建','西藏','贵州','辽宁','重庆','陕西','青海','黑龙江']

District_PinYin_Map =  {
		'上海':'shang_hai','云南':'yun_nan','内蒙古':'nei_meng_gu','北京':'bei_jing',
		'吉林':'ji_lin','四川':'si_chuan','天津':'tian_jin','宁夏':'ning_xia','安徽':'an_hui',
		'山东':'shan_dong','山西':'shan_xi','广东':'guang_dong','广西':'guang_xi','新疆':'xin_jiang',
		'江苏':'jiang_su', '江西':'jiang_xi','河北':'he_bei','河南':'he_nan','浙江':'zhe_jiang',
		'海南':'hai_nan',  '湖北':'hu_bei','湖南':'hu_nan','甘肃':'gan_su','福建':'fu_jian',
		'西藏':'xi_zang',  '贵州':'gui_zhou','辽宁':'liao_ning','重庆':'chong_qing','陕西':'shann_xi',
		'青海':'qing_hai', '黑龙江':'hei_long_jiang'}
PinYin_District_Map = dict((v,k) for k,v in District_PinYin_Map.iteritems())

CategoryPattern =  ["文%", "理%"]
CategoryList = ["文科","理科"]
CategoryMap = {"art":"文科","phy":"理科","文科":"文科","理科":"理科","理工":"理科"}
GaoKaoZongFeng={u'上海':630,u'海南':900,u'浙江':810,u'江苏':480, u'all':750}

def getStandardCategoryName(category):
	if category in CategoryMap:
		return CategoryMap[category]
	else:
		return category

def getDistrictName_Chn(district):

	if district in DistrictList:
		return district
	if district in PinYin_District_Map:
		return PinYin_District_Map[district]
	return None

def GetZongFen(curDistrict):
   if curDistrict in GaoKaoZongFeng:
	   return GaoKaoZongFeng[curDistrict]
   else:
	   return 750

#  Function getSchoolProb_Internal
#  This function calculates the probability for a student to get admission to a school using history recruiting data. Student must know his/her rank in current year.
#
#  Todo: need to reduce database query operations. This should involve table optimization.
#
#	Parameters:
#		eprint	[in] Logger function
#		db      [in] Mysql database connection
#		cursor  [in] SQL object for executing SQL statements
#		stuD    [in] Dictionary for passing student/school information and returnning probability for a school
#			'district': district
#			'year':current year
#			'category': art or physics
#			'rank': student rank in current year
#			'school': target school
#			'prob': Probability to get admission for target school.
#		bStdout	[in] If true, output probability to stdout If false, return quietly.
#   Searching previous year data for target school: 'high': highest score 'average': average score 'low': lowest score 'rc': recruiting number
#	Return: 0, failed 1 OK

def getSchoolProb_Internal(eprint, db, cursor, stuD, bStdout=False):
	# get score 'prevScore' in previous year: search in earlier score distribution table with the rank we get above to get score with the same rank in previous year
	sqlStr = "select * from %s where district='%s' and year='%d' and category='%s' and accumulation>=%d and accumulation-count<%d" % (\
		EGKConfig.dbTblCfg['tbl_score_distribution'], #default table:scores_distribution_by_province
		stuD['district'], int(stuD['year'])-1, stuD['category'], int(stuD['rank']), int(stuD['rank']))
	eprint ("get score in prev year - sql: %s" % sqlStr)
	cursor.execute(sqlStr)

	data = cursor.fetchall()
	eprint( "scores range : %s" %  data)

	if len(data) == 0:
		EGK_GetLogger().error( '{"ERROR":"Not found in history record. SQL:%s"}' % (sqlStr))
		sys.exit(-11)
	elif len(data) > 1:
		EGK_GetLogger().error( '{"ERROR":"Multiple entries found history record. SQL:%s"}' % (sqlStr))
		sys.exit(-12)

	high = data[0]["highest_score"]
	low = data[0]["lowest_score"]
	convertedScore = float((float(high)+low)/2)

	# get target school data: highest score/average score for previous year. DB Table:school_cutoff_scores_2008_2015
	sqlStr = "select school_name,district,category,round,year,highest_score,average_score \
		from %s \
		where district='%s' and category='%s' and year='%d' and school_name='%s' and round not like '%s' \
		group by district, category, year, school_name, round" % (\
		EGKConfig.dbTblCfg['tbl_school_cutoff_scores'], #default table:school_cutoff_scores_2008_2015
		stuD['district'],
		stuD['category'],
		int(stuD['year'])-1,
		stuD['school'], "%%提前%%")
	eprint("Find scores for previous year for school in district -sql: %s" % sqlStr)
	cursor.execute(sqlStr)
	prevSchScore = cursor.fetchall()
	eprint("Scores for school: %s" % prevSchScore)

	closestIdx = 0
	if len(prevSchScore) == 0:
		EGK_GetLogger().error( '{"ERROR":"Can not find scores sql: %s" }' % (sqlStr))
		return 0
		#sys.exit(-1002)
	elif len(prevSchScore) > 1:
		minScoreDiff = 1000
		eprint( '{"WARNING":"Multiple entries in cutoff score table year:%d district:%s"}' % (int(stuD['year'])-1, stuD['district']))
		for i,v in enumerate(prevSchScore):
			eprint ("school %d: district:%s category:%s year:%d school:%s highest_score:%s average_score:%s round:%s" % (\
				i, v['district'], v['category'], v['year'], v['school_name'], v['highest_score'], v['average_score'], v['round']))
			if abs(v['average_score'] - convertedScore) < minScoreDiff:
				minScoreDiff = abs(v['average_score'] - convertedScore)
				closestIdx = i
		EGK_GetLogger().debug("closestIdx:%d" % (closestIdx))


	prevHighScore = prevSchScore[closestIdx]["highest_score"]
	prevAvgScore  = prevSchScore[closestIdx]["average_score"]

	# get recruiting number of target school. Assuming it is a similar sequence over year. We'll use this number to adjust probability.
	sqlStr = "select school_name,year,category,district,degree,sum(recruiting_number) as rc_num from %s \
		where year='%d' and district='%s' and category='%s' and school_name='%s' \
		group by degree" % (\
		EGKConfig.dbTblCfg['tbl_recruiting_plan'], #default table: recruiting_plan_m_2015_good
		int(stuD['year'])-1, stuD['district'], stuD['category'], stuD['school'])
	eprint("Get recruiting num - sql: %s" % sqlStr)
	cursor.execute(sqlStr)
	prevRcPlan = cursor.fetchall()
	eprint("Recruiting plan: %s" % prevRcPlan)

	prevRcNum = 0
	if len(prevRcPlan) == 0:
		EGK_GetLogger().error ( '{"ERROR": "Recruiting plan not found. Give an average number: 15. SQL:%s" }' % (sqlStr))
		prevRcNum = 15
		#sys.exit(-1004)
	elif len(prevRcPlan) > 1:
		EGK_GetLogger().debug ( '{"WARNING": "Multiple recruiting entries. TBD. SQL:%s" }' %(sqlStr) )
		EGK_GetLogger().debug("INFO: list prevRcPlan length:%d idx:%d" % (len(prevRcPlan),closestIdx))
		closestMatchIdx = -1
		maxMatchingLen = 1
		for i,v in enumerate(prevRcPlan):
			EGK_GetLogger().debug("school:%s %s %s %s %s recruiting:%d" %(
				v['school_name'], v['year'], v['district'], v['category'], v['degree'], v['rc_num']))
			EGK_GetLogger().debug("matching length:%d" %(len(set(v['degree']).intersection(prevSchScore[closestIdx]['round']))))
			if len(set(v['degree']).intersection(prevSchScore[closestIdx]['round'])) > maxMatchingLen:
				closestMatchIdx = i
				maxMatchingLen = len(set(v['degree']).intersection(prevSchScore[closestIdx]['round']))
				prevRcNum = float(v['rc_num'])
				break
		else:
			EGK_GetLogger().error( '{"ERROR": "Can not find valid match between recruiting plan and scores for %s"' % (sqlStr))
			sys.exit(-1)

		EGK_GetLogger().debug("Select closest match. rcnum:%d degree:%s" % (prevRcNum, prevRcPlan[closestMatchIdx]['degree']))
		# Assume the order is same as cutoff score table
		#prevRcNum = float(prevRcPlan[closestIdx]['rc_num'])
		#~ sys.exit(-1005)
	else:
		prevRcNum = float(prevRcPlan[0]["rc_num"])

	# get school rank in prev year
	sqlStr = "select school_name, rank, prev_rank \
		from %s where school_name='%s'" %(
		EGKConfig.dbTblCfg['tbl_school_rank_by_general'], #Default table:school_rank_2015_airay
		stuD['school'])
	eprint("Get school rank sql: %s" % sqlStr)
	cursor.execute(sqlStr)
	rankInfo = cursor.fetchall()
	eprint("School rank: %s" % rankInfo)

	if len(rankInfo) == 0:
		EGK_GetLogger().error ( '{"ERROR": "School rank not found. SQL:%s" }' % (sqlStr) )
		#~ sys.exit(-1004)
	elif len(rankInfo) > 1:
		EGK_GetLogger().error ( '{"ERROR": "Multiple entries in school rank. TBD. SQL:%s" }' % (sqlStr))
		sys.exit(-1005)

	#get school rank by average score in that district
	#~ schoolRankTbl = "school_cutoff_scores_by_y_m_src2_uniq"
	#~ sqlStr = 'select school_name,district,category,round,highest_score,average_score,lowest_score,AVG(average_score) \
		#~ from %s \
		#~ where year=%d and category="%s" and district="%s" \
		#~ group by school_name,round order by AVG(average_score) desc' % (schoolRankTbl, int(stuD['year'])-1, stuD['category'], stuD['district'])
	schoolRankTbl = EGKConfig.dbTblCfg['tbl_school_rank_by_score'] #default table:"school_rank_by_score"
	sqlStr = 'select school_name,district,category,round,highest_score,average_score,lowest_score,sub_rank \
		from %s \
		where year=%d and category="%s" and district="%s" and school_name="%s"' % (
		schoolRankTbl, int(stuD['year'])-1, stuD['category'], stuD['district'], stuD['school'])

	eprint("Get school rank by average score - sql: %s" % sqlStr)
	cursor.execute(sqlStr)
	eprint("sql done")
	scoreRankInfo = cursor.fetchall()
	eprint("School rank by score average-total schools: %d" % len(scoreRankInfo))

	schScoreRankItem = None
	schScoreRankIdx = -1
	for i,v in enumerate(scoreRankInfo):
		#eprint (i, v, stuD['school'])
		if v['school_name'].encode('utf8') == stuD['school']:
			schScoreRankItem = v
			schScoreRankIdx = i
			eprint ("Found rank in table by average score: %s" % schScoreRankIdx)
			break
	if schScoreRankItem == None:
		EGK_GetLogger().error('{"ERROR": "Can not find school rank in recruiting data for last year. SQL:%s"}' %(sqlStr))
		sys.exit(-1006)

	highLowRatio = 0.0
	if prevRcNum == 1:
		highLowRatio = 0.0
	elif prevRcNum == 2:
		highLowRatio = 1.0
	elif prevRcNum < 10:
		highLowRatio = 0.8
	elif prevRcNum < 60:
		highLowRatio = 0.7
	elif prevRcNum < 110:
		highLowRatio = 0.55
	else:
		highLowRatio = 0.5

	estimatedLowScore = float(prevAvgScore) - (prevHighScore - prevAvgScore) * highLowRatio

	# Assume n is the score, (low, average, high) represents the lowest/average/high scores of the accepted applicants for a school.the probability will be computed by:
	# 1. [0, low-100): base points: 10. Minimum score for any applicant.
	# 2. [low-100,low): adjusted points: max 30.  y = 0.3*(n+100-low).
	# 3. [low, low+2/3*(average-low)): 10.
	# 4. [low+2/3*(average-low), average]: [10,35].
	# 5. [average, high]: [35,40].
	# 6. [high, max]: 3.
	# 7. 3/4/5/6/ will multiply by rc plan factor: bigger recruiting number means more probability.
	# 7.1 recruiting number in [1,100]:  0.4-1.4: 1@0.4, 50@1.00, 100@1.4  with 60 @ 1.00 [110,300), [1.5,1.6].
	# 8. Overall prob: max 98.

	prob = 0.0
	if convertedScore < estimatedLowScore-100:
		prob = 10.0
		eprint("<low-100:%5.3f" % prob)
	elif convertedScore < estimatedLowScore:
		prob = 10.0+ 0.3 * (convertedScore+100-estimatedLowScore)
		eprint("<low:%5.3f" % prob)
	elif float(convertedScore) < float(estimatedLowScore)+1/3*(prevAvgScore-estimatedLowScore):
		prob = 40.0 + 10.0 / (2/3 * (prevAvgScore-estimatedLowScore)) * (convertedScore-estimatedLowScore)
		eprint("<low+1/3diff:%5.3f" % prob)
	elif convertedScore < prevAvgScore:
		prob = 50.0 + float(convertedScore-estimatedLowScore)/(prevAvgScore-estimatedLowScore) * 30.0
		eprint("<avg:%5.3f" % prob)

	elif convertedScore < prevHighScore:
		prob = 80.0 + float(convertedScore-prevAvgScore)/(prevHighScore-prevAvgScore)*5.0
		eprint("<high:%5.3f" % prob)
	else:
		prob = 90.0 + (convertedScore-prevHighScore)*0.01
		eprint(">=high:%5.3f" % prob)

	eprint ("original prob:%5.3f" % prob)

	# multiply factor calculated from recruiting number
	mf=0.5
	if prevRcNum<1:
		mf=0.0
		prob=0.0
	elif prevRcNum < 101:
		mf=0.95 + prevRcNum * 0.01
	elif prevRcNum < 1101:
		mf=1.5 + (prevRcNum-100)*0.0001
	else:
		mf=1.7

	if prob>60.0:
		prob = 60.0 + (prob-60.0)*mf

	if prob>99.0:
		prob = 99.0

	if int (stuD['rank']) < int(prevRcNum * 1.5):
		prob = 100.0

	eprint ("My score:%d my rank:%d rc plan:%d high:%d average:%d low:%d prob:%6.3f multiply factor:%5.3f" % \
		(convertedScore, stuD['rank'], prevRcNum, prevHighScore, prevAvgScore, estimatedLowScore, prob, mf))

	if bStdout == True:
		print ('{"score":"%d","rank":"%d","school":"%s","year":"%s","district":"%s","prob":"%.0f"}' % \
			(stuD['score'], stuD['rank'], stuD['school'], stuD['year'], stuD['district'], prob))

	stuD['prob'] = prob
	return 1
	#end of funciton getSchoolProb()

def getSchoolProb(stuD, bStdout=False):
	return getSchoolProb_Internal(eprint,  EGK_GetDbConn(), EGK_GetDbCursor(), stuD, bStdout)

def getSchoolProb_V2(stuD, rcRecord, bStdout=False):
	prevRcNum = rcRecord['recruit_num_total']
	estimatedLowScore = rcRecord['lowest_score']
	prevAvgScore = rcRecord['average_score']
	prevHighScore = rcRecord['highest_score']
	convertedScore = stuD['prevScore']

	# Assume n is the score, (low, average, high) represents the lowest/average/high scores of the accepted applicants for a school.the probability will be computed by:
	# 1. [0, low-100): base points: 10. Minimum score for any applicant.
	# 2. [low-100,low): adjusted points: max 30.  y = 0.3*(n+100-low).
	# 3. [low, low+2/3*(average-low)): 10.
	# 4. [low+2/3*(average-low), average]: [10,35].
	# 5. [average, high]: [35,40].
	# 6. [high, max]: 3.
	# 7. 3/4/5/6/ will multiply by rc plan factor: bigger recruiting number means more probability.
	# 7.1 recruiting number in [1,100]:  0.4-1.4: 1@0.4, 50@1.00, 100@1.4  with 60 @ 1.00 [110,300), [1.5,1.6].
	# 8. Overall prob: max 98.

	prob = 0.0
	if convertedScore < estimatedLowScore-100:
		prob = 10.0
		eprint("<low-100:%5.3f" % prob)
	elif convertedScore < estimatedLowScore:
		prob = 10.0+ 0.3 * (convertedScore+100-estimatedLowScore)
		eprint("<low:%5.3f" % prob)
	elif float(convertedScore) < float(estimatedLowScore)+1/3*(prevAvgScore-estimatedLowScore):
		prob = 40.0 + 10.0 / (2/3 * (prevAvgScore-estimatedLowScore)) * (convertedScore-estimatedLowScore)
		eprint("<low+1/3diff:%5.3f" % prob)
	elif convertedScore < prevAvgScore:
		prob = 50.0 + float(convertedScore-estimatedLowScore)/(prevAvgScore-estimatedLowScore) * 30.0
		eprint("<avg:%5.3f" % prob)

	elif convertedScore < prevHighScore:
		prob = 80.0 + float(convertedScore-prevAvgScore)/(prevHighScore-prevAvgScore)*5.0
		eprint("<high:%5.3f" % prob)
	else:
		prob = 90.0 + (convertedScore-prevHighScore)*0.01
		eprint(">=high:%5.3f" % prob)

	eprint ("original prob:%5.3f" % prob)

	# multiply factor calculated from recruiting number
	mf=0.5
	if prevRcNum<1:
		mf=0.0
		prob=0.0
	elif prevRcNum < 101:
		mf=0.95 + prevRcNum * 0.01
	elif prevRcNum < 1101:
		mf=1.5 + (prevRcNum-100)*0.0001
	else:
		mf=1.7

	if prob>60.0:
		prob = 60.0 + (prob-60.0)*mf

	if prob>99.0:
		prob = 99.0

	if int (stuD['rank']) < int(prevRcNum * 1.5):
		prob = 100.0

	eprint ("My score:%d my rank:%d rc plan:%d high:%d average:%d low:%d prob:%6.3f multiply factor:%5.3f" % \
		(convertedScore, stuD['rank'], prevRcNum, prevHighScore, prevAvgScore, estimatedLowScore, prob, mf))

	if bStdout == True:
		print ('{"score":"%d","rank":"%d","school":"%s","year":"%s","district":"%s","prob":"%.0f"}' % \
			(0, stuD['rank'], stuD['school'], stuD['year'], stuD['district'], prob))

	stuD['prob'] = prob
	return 1
	#end of funciton getSchoolProb_V2()


def getSchoolProb_V2_1(stuD, schModel, bStdout = False):
	stuSegs = [[]]
	if isinstance(schModel['segment_mdl'],basestring):
		stuSegs = ast.literal_eval(schModel['segment_mdl'])
		#~ EGK_GetLogger().debug("segment model:%s" % (stuSegs))
	else:
		stuSegs = schModel['segment_mdl']	# list of [id,studentNumber,lowrank,highrank,avgrank,randdev]
	# Find segs
	if stuD['rank'] < stuSegs[0][2]:
		# better than any students
		stuD['prob'] = 99
		stuD['class'] = 0
		stuD['behind'] = schModel['tot_rc']
		if schModel['tot_rc'] < 5:
			stuD['prob'] = 99 - (5-schModel['tot_rc'])
		return 1
	if stuD['rank'] > stuSegs[-1][3]: # worse than any students recruited
		ratio = float(stuD['rank']) / stuSegs[-1][3]
		if ratio < 1.05:
			stuD['prob'] = 50
		elif ratio < 2.05:
			stuD['prob'] = 50 - (ratio-1.05) * 40
		elif ratio < 12.05:
			stuD['prob'] = 10 - (ratio-2.05)
		stuD['class'] = 4
		stuD['behind'] = 0
		return 1

	stuClass = -1
	for i,seg in enumerate(stuSegs):
		if stuD['rank']<= seg[3]:
			stuClass = i
			break
	else:
		stuClass = 5
	prob = 50.0 + (4-stuClass)*10 #assign a base prob
	#~ EGK_GetLogger().debug("base prob:%d" % (prob))
	#Rules:
	#1.if student's rank is higher than 80% of the people, prob = 80%
	#2.50% rule: if student's rank is in the last rank cluster extend the cluster to same class
	#. if number of students in lowest cluster is small, <5%, or <2
	#.
	adj = 0.0
	stuBehind = sum(v[1] for v in stuSegs[stuClass+1:])
	if stuClass == len(stuSegs)-1 and stuSegs[-1][1]<2:
		adj += -5
	else:
		adj += (stuBehind+stuSegs[stuClass][1])-5
	#~ EGK_GetLogger().debug("  adjust by student number below:%.2f" % (adj))

	adj1 = (float(schModel['tot_rc']) - 10.0)/30
	if adj1 > 5.0:
		adj1 = 5.0
	#~ EGK_GetLogger().debug("  adjust by total number below:%.2f" % (adj1))

	adj += adj1
	prob += adj
	if float(prob) > 99.0:
		prob = 99.0
	stuD['prob'] = prob
	stuD['class'] = stuClass
	stuD['behind'] = stuBehind
	return 1
	#end of getSchoolProb_V2_1

def getScoreByRank(logger, db, cursor, district, category, year, rank):
	sqlStr = "select * from %s where district='%s' and year='%s' and category='%s' and accumulation>=%d and accumulation-count<%d" % (\
	EGKConfig.dbTblCfg['tbl_score_distribution'], #default table:scores_distribution_by_province
	district, year, category, rank, rank)
	logger.debug ("get score by rank:%s" % (sqlStr))
	cursor.execute(sqlStr)

	data = cursor.fetchall()

	if len(data) == 0:
		EGK_GetLogger().error( '{"ERROR":"getScoreByRank()-Not found history record. SQL:%s"}' % (sqlStr))
		sys.exit(-11)
	elif len(data) > 1:
		EGK_GetLogger().error( '{"ERROR":"Multiple entries in history record. SQL:%s"}' %(sqlStr))
		sys.exit(-12)

	high = data[0]["highest_score"]
	low = data[0]["lowest_score"]

	scoreDiff = high - low
	if data[0]["rank"] == 1:
		score = low + (data[0]['count'] - rank)
		if score > high:
			score = high
		logger.debug("convert outstanding rank %d to score %d" % (rank, score))
		return score
	return (high+low)/2

def getRankByScore(logger, db, cursor, district, category, year, score):
	if score > GetZongFen(district):
		print('{"ERROR":"getRankByScore() - Score %d is bigger than max."}' % (score), file=sys.stderr )
		return 1

	if score < 0:
		print ('{"ERROR":"Negative score %d - impossible!"}' % (score), file=sys.stderr)
		sys.exit(-1)

	rankSqlStr = "select * from %s where district='%s' and year='%s' and category='%s' and lowest_score<=%d ORDER BY `accumulation` ASC limit 1" % (\
		EGKConfig.dbTblCfg['tbl_score_distribution'], #default table:scores_distribution_by_province
		district, year, category, score)
	logger.debug("getRankByScore() - sql: %s" % (rankSqlStr))
  	cursor.execute(rankSqlStr)
	rankData = cursor.fetchall()
	logger.debug( "getRankByScore() - scores range : %s" %  rankData)

	if len(rankData) == 0:
		logger.debug ('{"ERROR":"getRankByScore() - No rank information for score. Please check database table. SQL:%s"}' % (rankSqlStr) )
		predictSql = "select district, year, category, count(*) as rows, max(accumulation) as last_rank, \
			sum(count) as total_students,max(highest_score) as high,min(lowest_score) as low,\
			sum(count)/(max(highest_score)-min(lowest_score)+1) as average_num from \
				(select * from %s \
					where  district='%s' and year='%s' and category='%s' order by accumulation desc limit 10 ) as t1" %(
			EGKConfig.dbTblCfg['tbl_score_distribution'], #default table:scores_distribution_by_province
			district, year, category)
		logger.debug("getRankByScore() - sql for prediction: %s" % (predictSql))
		cursor.execute(predictSql)
		predictData = cursor.fetchall()
		logger.debug( "getRankByScore() - scores range : %s" %  predictData)
		if len(predictData) != 1:
			logger.error("Error: Can't get data for predicting rank by score")
			sys.exit(-1)

		pv = predictData[0]
		pvRank = int(pv['last_rank'] + pv['average_num'] * (pv['low'] - score))
		logger.debug("Guess rank %d for score %d - student number per score:%.2f last rank:%s last score:%s" %(
			score, pvRank, pv['average_num'], pv['last_rank'], pv['low']))
		return pvRank

	elif len(rankData) > 1:
		logger.error ('{"ERROR":"getRankByScore() - Multiple rank entries for a single score.Please check database table. SQL:%s"}' % (rankSqlStr) )
		sys.exit(-10)

	scoreDiff = rankData[0]['highest_score'] - rankData[0]['lowest_score']
	if rankData[0]["rank"] == 1:
		rank = rankData[0]['accumulation'] - (score - rankData[0]['lowest_score'])
		if rank < 1:
			rank = 1
		logger.debug("convert outstanding score %d to rank %d" % (score,rank))
		return rank
	if scoreDiff > 1:
		logger.debug("convert score to rank using linear interpolation for score range %d>1" % (scoreDiff))
		return int (rankData[0]['accumulation'] - float(rankData[0]['count']-1) * (float(score) - float(rankData[0]['lowest_score'])) / scoreDiff)
	return rankData[0]["accumulation"]

# Function: getScoreByDiff
#
# Compute real score when score difference is given by looking up cutoff score table.
# Problem: Not finished. We just assume this is difference above BenKeYiPi. Need to lookup all of them.
#
def getScoreByDiff(diffStr):
	diffList = diffStr.split(':')
	args = EGKConfig.cmdArgs
	logger = EGK_GetLogger()

	diffSql = "select * from %s where district='%s' and category='%s' and year='%s' and round='%s'" % (\
	EGKConfig.dbTblCfg['tbl_cutoff_scores'], #default table: district_cutoff_scores_by_round
	args.district, args.category, args.year, diffList[0])

	eprint("getScoreByDiff: diff def:[%s] sql:[%s]" % (diffStr, diffSql))

	EGK_GetDbCursor().execute(diffSql)
	data = EGK_GetDbCursor().fetchall()

	if len(data) != 1:
		raise ValueError ('{"ERROR":"Invalid round specifier %s when searching. SQL:%s"' % (diffSql))

	rec = data[0]
	cutoffScore = rec["cutoff_scores"]
	curScore = int(cutoffScore) + int(diffList[1])
	eprint("Real score: %d diff:%s cutoff:%s" % (curScore, diffList[1], cutoffScore))
	return curScore

