#!/usr/bin/env python
# encoding: utf-8
# @Author: zhoubo(congminghaoxue@gmail.com)

from fabric.api import local,cd,run, env

env.hosts=['bzhou@192.168.2.228:22',] #ssh要用到的参数
env.password = 'bz-2016-1125'


def update_backend():
    print "update Backend code to aliyun"
    with cd('~/'):   #cd用于进入某个目录
        run('sh /data/backend-git-pull-gerrit-push-ali.sh')  #远程操作用run
def deploy():
    print('update all code to aliyun')
    run('sh /data/git-pull-gerrit-push-ali.sh')
