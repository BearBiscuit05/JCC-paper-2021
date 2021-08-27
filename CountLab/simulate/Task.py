#!  conda env
# -*- coding:utf-8 -*-
# Time:2021/3/24 上午11:09
# Author : nishizzma
# File : Task.py

import time
import numpy as np
import math

class Task:
    uid = 0
    def __init__(self,str):
        self.uid = Task.uid
        Task.uid += 1
        self.comeTime = time.time()
        self.startTime = 0  # 任务响应时间
        self.endTime = 0  # 任务结束时间
        self.attr = str

        self.countFLOPsAndParam(str)

    def setIndex(self,num,batchsize,epoch):
        self.num = num
        self.batchsize = batchsize
        self.epoch = epoch


    def countFLOPsAndParam(self,str):
        if str == "alex":
            #单张图片的计算量
            self.FLOPs = 1.42e+9
            self.param = 4*6.11e+7
            self.singletime = 507.7

            #设置为全局的batchsize
        if str == "vgg11":
            self.FLOPs = 2*7.74e+9
            self.param = 4*132.86e+6
            self.singletime = 635.7

        if str == "resnet18":
            self.FLOPs = 2*1.82e+9
            self.param = 4*11.69e+6
            self.singletime = 718.9

        if str == "googlenet":
            self.FLOPs = 3.1e+9
            self.param = 4*6.6e+6
            self.singletime = 1610.5

        if str == "self_1":
            self.FLOPs = 1.01e+9
            self.param = 4*400.36e+6
            self.singletime = 740.2

        if str == "self_2":
            self.FLOPs = 2.2e+9
            self.param = 4*802.36e+6
            self.singletime = 780.3

        if str == "self_3":
            self.FLOPs = 0.6e+9
            self.param = 730.36e+6
            self.singletime = 440


    def countBatchsize(self,num):

        if num >2000:
            self.batchsize = np.random.choice([126,256,300,400,512,600,1024])
        if num <2000:
            self.batchsize = np.random.choice([126,200,256,512])
            if num < self.batchsize:
                self.batchsize = num


    def countFLOPs(self):
        return self.FLOPs*self.num

    def countIter(self,GPUNUM):
        return max(math.ceil(self.num/(self.batchsize*GPUNUM)),1)
        # return max(int(self.num / (self.batchsize)), 1)

    def countBatchsize(self,GPUNUM):
        return self.batchsize/GPUNUM

    def countComm(self,GPUNUM):
        """
        :return:计算总通信量
        """
        self.countIter(GPUNUM)
        return self.param*self.countIter(GPUNUM)*self.epoch

    def usingTimeCount(self,gpu_P,gpuNum,BW):
        indexList = [1.0,0.50322,0.25465,0.13365,0.07168,0.04357,0.03167,0.02544,0.02286,0.02154]
        index = indexList[int(np.log2(self.batchsize))]*self.singletime*self.countIter(gpuNum)*self.epoch
        if gpuNum == 1:
            print("在{}个GPU环境下，计算时间为{},通讯时间为{}".format(gpuNum, index, 0))
            return  index

        print("在{}个GPU环境下，计算时间为{},通讯时间为{}".format(gpuNum,index,self.countComm(gpuNum)/BW))
        return index + self.countComm(gpuNum)/BW

        # indexList = [1.0, 0.50322, 0.25465, 0.13365, 0.07168, 0.04357, 0.03167, 0.02544, 0.02286, 0.02154]
        # index = indexList[int(np.log2(self.batchsize / gpuNum))] * self.singletime * self.countIter(gpuNum) * self.epoch
        # if gpuNum == 1:
        #     print("在{}个GPU环境下，计算时间为{},通讯时间为{}".format(gpuNum, index, 0))
        #     return index
        #
        # print("在{}个GPU环境下，计算时间为{},通讯时间为{}".format(gpuNum, index, self.countComm(gpuNum) / BW))
        # return index + self.countComm(gpuNum) / BW

    def endTimeCount(self,gpu_P,gpuNum,BW):
        """
        :param gpu_P:
        :param gpuNum:
        :param BW:
        :return: 计算在集群中所需要花费的总时间
        """
        #倍化
        return time.time()+self.usingTimeCount(gpu_P,gpuNum,BW)/100

    def maxAccessGPU(self):
        if self.num%self.batchsize == 0:
            return int(self.num / self.batchsize)
        return int(self.num/self.batchsize) + 1

    def showTask(self):
        print('\033[1;34m'+
              "[Task-{}:id:{}]:FLOPs:{},NUM:{},batchsize:{},epoch:{}"
              .format(self.attr,self.uid,self.FLOPs,self.num,self.batchsize,self.epoch)+ '\033[0m')
