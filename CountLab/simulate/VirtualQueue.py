#!  conda env
# -*- coding:utf-8 -*-
# Time:2021/3/24 下午5:09
# Author : nishizzma
# File : VirtualQueue.py

class VirtualQueue:
    ell = 5e+11
    def __init__(self):
        self.task_len = 0

    def addLen(self, len):
        self.task_len += VirtualQueue.ell - len

    def deleteLen(self):
        self.task_len =  self.task_len/2

    def showLen(self):
        return self.task_len
