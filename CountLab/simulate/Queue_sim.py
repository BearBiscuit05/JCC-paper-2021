#!  conda env
# -*- coding:utf-8 -*-
# Time:2021/3/24 下午5:00
# Author : nishizzma
# File : Queue_sim.py
from simulate.Task import Task
from simulate.Cluster import Cluster
import time

class Queue_sim:
    def __init__(self):
        self.task_list = []
        self.task_len = 0

    def addTask(self,task):
        task.showTask()
        self.task_list.append(task)
        self.addLen(task.countFLOPs())

    def deleteTask(self,task):
        self.task_list.remove(task)
        self.deleteLen(task.countFLOPs())

    def addLen(self,len):
        self.task_len += len

    def deleteLen(self,len):
        self.task_len = max(self.task_len-len,0)

    def showLen(self):
        return self.task_len

    def showTask(self):
        return self.task_list
