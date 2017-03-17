#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import os
import sys, getopt, argparse
import mysql.connector
import string
import encodings,codecs
import random
from operator import itemgetter,attrgetter,methodcaller
import logging

from ConfigParser import ConfigParser
import io


class EGKConfig(ConfigParser):
	dbConnCfg = {}
	dbTblCfg = None
	dbConn = None
	cmdArgs = {}
	logger = None
	logCfg = None

	def __init__(self, args, allow_no_value=True, connectDB=True):
		ConfigParser.__init__(self)

		EGKConfig.cmdArgs = args
		myCfgFile = EGKConfig.cmdArgs.config
		cfgFiles = self.read(myCfgFile)
		if len(cfgFiles) == 0:
			raise ValueError("Configuration file %s not found" % (myCfgFile))
		EGKConfig.logCfg = dict(self.items('general'))
		logfile = EGKConfig.logCfg['logfile'].strip()
		if len(logfile) > 0:
			logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s', filename=logfile)
		else:
			logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s')
		EGKConfig.logger = logging.getLogger("EGK")
		if args.verbose != None:
			EGKConfig.logger.setLevel(int(args.verbose))
		else:
			EGKConfig.logger.setLevel(int(EGKConfig.logCfg['loglevel'].strip()))

		EGKConfig.logger.debug( os.environ.get("PYTHONIOENCODING"))
		if os.environ.get("PYTHONIOENCODING") != "utf-8":
			EGKConfig.logger.error ("You must set environement variable PYTHONIOENCODING to utf-8: export PYTHONIOENCODING=utf-8")
			EGKConfig.logger.error ("Use: export PYTHONIOENCODING=utf-8 && your-command args...")
			sys.exit(-1)

		if connectDB == False:
			EGKConfig.logger.debug("Bare configuration initialization. No DB connection.")
			return

		EGKConfig.dbConnCfg = dict(self.items("mysql"))
		EGKConfig.dbTblCfg  = dict(self.items("database"))
		EGKConfig.dbConn = mysql.connector.connect(
			host=EGKConfig.dbConnCfg['host'],
			user=EGKConfig.dbConnCfg['user'],
			password=EGKConfig.dbConnCfg['password'],
			database=EGKConfig.dbTblCfg['database'])
		EGKConfig.dbCursor = EGKConfig.dbConn.cursor(dictionary=True)
		EGKConfig.logger.debug("Database:%s Host:%s" % (EGKConfig.dbTblCfg['database'], EGKConfig.dbConnCfg['host']))

	def __del__(self):
		if EGKConfig.dbConn != None:
			EGKConfig.dbConn.close()
			EGKConfig.dbConn = None
	def as_dict(self):
		d = dict(self._sections)
		for k in d:
			d[k] = dict(self._defaults, **d[k])
			d[k].pop('__name__', None)
		return d
	def dump(self):
		print ("Definitions for database connection:%s" % (EGKConfig.dbConnCfg))
		print ("Definitions for database tables:%s" % (EGKConfig.dbTblCfg))

def EGK_GetLogger():
	return EGKConfig.logger

def EGK_GetDbConn():
	return EGKConfig.dbConn

def EGK_GetDbCursor():
	return EGKConfig.dbCursor

def EGK_GetDbTblCfg():
	return EGKConfig.dbTblCfg

def eprint(*args, **kwargs):
	EGKConfig.logger.debug(*args, **kwargs)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Tool to get a list of possible schools given district/category/score")
	parser.add_argument('-v', '--verbose',  required=False, default='20', help="Message level. 10:'DEBUG'/20:'INFO'/30:'WARNING'/40:'ERROR'/50:'CRITICAL'")
	parser.add_argument('--config', default='./egk.ini', help="the configuraiton file")
	args = parser.parse_args()

	config = EGKConfig(args, allow_no_value=True)

	#List all contents
	EGK_GetLogger().debug("Configuration file:")
	print(config.as_dict())
	config.dump()

	del config
