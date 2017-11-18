#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-18 18:18:56
# @Author  : Zhou Bo (congminghaoxue@gmail.com)
# @Link    : https://congminghaoxue.github.io/
# @Version : $Id$


try:
    from chardet.universaldetector import UniversalDetector
    IsAuto = True
except  ImportError:
    IsAuto = False
import os
import os.path
import glob
def Convert_Auto( filename,out_enc="utf-8" ):
    ''' Re-encode text file with auto detec current encode. Need chardet Lib.
        Input Parameter:
        filename: full path and file name, e.g. c:/dir1/file.txt
        out_enc: new encode. Default as 'utf-8'
        Output Parameter
        None'''
    try:
        with open(filename,'rb') as f:
            b= b' '
            b+=f.read(1024)
            u=UniversalDetector()
            u.reset()
            u.feed(b)
            u.close()
            f.seek(0)
            b=f.read()
            in_enc=u.result['encoding']
            new_content=b.decode(in_enc, 'ignore')
        with open(filename, 'w', encoding=out_enc) as f:
            f.write(new_content)

        print ("Success: "+filename+" converted from "+ in_enc+" to "+out_enc +" !")
    except IOError:
        print ("Error: "+filename+" FAIL to converted from "+ in_enc+" to "+out_enc+" !" )
def Convert_Manu( filename,in_enc='gbk', out_enc="utf-8" ):
    ''' Re-encode text file with manual decide input text encode.
        Input Parameter:
            filename: full path and file name, e.g. c:/dir1/file.txt
            in_enc:  current encode. Default as 'gbk'
            out_enc: new encode. Default as 'utf-8'
        Output Parameter
            None
        '''
    try:
        print ("convert " + filename)
        with open(filename,'rb') as f:
            b=f.read()
            new_content=b.decode(in_enc, 'ignore')
        with open(filename, 'w', encoding=out_enc) as f:
            f.write(new_content)

        print ("Success: "+filename+" converted from "+ in_enc+" to "+out_enc +" !")
    except IOError:
        print ("Error: "+filename+" FAIL to converted from "+ in_enc+" to "+out_enc+" !" )

def explore(dir, IsLoopSubDIR=True, suffix):
    '''Convert files encoding.
        Input:
            dir         : Current folder
            IsLoopSubDIR:   True -- Include files in sub folder
                            False-- Only include files in current folder
        Output:
            NONE
    '''
    if IsLoopSubDIR:
        flist=getSubFileList(dir, suffix)
    else:
        flist=getCurrFileList(dir, suffix)
    for fname in flist:
        if IsAuto:
            Convert_Auto(fname, 'utf-8')
        else:
            Convert_Manu(fname, 'gbk', 'utf-8')

def getSubFileList(dir, suffix=''):
    ''' Get all file list with specified  suffix under current folder(Include sub folder)
        Input:
            dir     :   Current folder
            suffix  :   default to blank, means select all files.
        Output:
            File list
    '''
    flist=[]
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name.endswith(suffix):
                flist.append(os.path.join(root,  name))
    return flist
def getCurrFileList(dir, suffix=''):
    ''' Get all file list with specified suffix under current level folder
        Input:
            dir     :   Current folder
            suffix  :   default to blank, means select all files.
        Output:
            File list
    '''
    if suffix=='':
        files=glob.glob('*')
    else:
        files=glob.glob('*'+suffix)
    flist=[]
    for f in files:
        flist.append(os.path.join(dir, f))
    return flist


def main():
    file_path='/Users/zhoubo/Music/'
    suffix='cue'
    explore(file_path, True, suffix)

if __name__ == "__main__":
   main()
