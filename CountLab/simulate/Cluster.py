#!  conda env
# -*- coding:utf-8 -*-
# Time:2021/3/24 上午11:10
# Author : nishizzma
# File : Cluster.py
from simulate.Task import Task
import time
import numpy as np

class Cluster:
    def __init__(self):
        self.GPUNUM = 8
        self.broadWith = 125e+6
        self.state = [0 for i in range(self.GPUNUM)]
        self.usingTime = [0 for i in range(self.GPUNUM)]
        self.taskId = [-1 for i in range(self.GPUNUM)]


    def gpu_p(self,batch):
        """
        :param batch:批处理大小
        :return: GPU算力
        """
        m = batch
        p = -0.3708*np.power(m,4) +355.7*np.power(m,3) - 1.065e+05*np.power(m,2) + 1.21e+07*m+ 1.964e+07
        return 100*p


    def idleGPU(self):
        """
        检测是否有空闲GPU，以及空闲GPU位置
        """
        count = 0
        idleList = []
        for i in range(self.GPUNUM):
            if self.state[i] == 0:
                count += 1
                idleList.append(i)
        return count,idleList


    def putTask(self,task,n):
        """
        将任务放置与n个GPU上
        """
        num ,gpulist = self.idleGPU()
        if  num < n:
            print("程序出错，任务无法被放置!!")
            return -1
        task.startTime = time.time()
        endtime = task.endTimeCount(self.gpu_p(task.batchsize),n,self.broadWith)
        task.endTime = endtime
        print('\033[1;32m'+"[放置任务] "+'\033[0m'+"task:{},使用GPU数目：{}，任务开始时间{}，任务结束时间{},任务需要时间:{}"
              .format(task.uid,n,time.asctime(time.localtime(task.startTime)),time.asctime(time.localtime(task.endTime)),task.endTime-task.startTime))
        for i in range(self.GPUNUM):
            if n>0 and self.state[i] == 0:
                self.state[i] = 1
                self.usingTime[i] = endtime
                self.taskId[i] = task.uid
                n -= 1

    def cleanTask(self,uid):
        """
        清楚以及完成的任务
        """
        temptime = 0
        for i in range(self.GPUNUM):
            if self.taskId[i] == uid:
                temptime = self.usingTime[i]
                self.state[i] = 0
                self.usingTime[i] = 0
                self.taskId[i] = -1
        print('\033[1;31m'+"[任务完成]" + '\033[0m'+" task:uid = {},当前空闲GPU数:{}".format(uid,self.idleGPU()))
        return uid

    def ifEmpty(self):
        """
        集群检测是否有过期任务
        """
        uids = []
        for i in range(self.GPUNUM):
            if self.usingTime[i]!=0 and self.usingTime[i] < time.time():
                uids.append(self.cleanTask(self.taskId[i]))
        return uids






