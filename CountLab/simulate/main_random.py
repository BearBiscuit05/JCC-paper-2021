#!  conda env
# -*- coding:utf-8 -*-
# Time:2021/3/24 下午4:48
# Author : nishizzma
# File : main.py

from simulate.Task import Task
from simulate.Cluster import Cluster
from simulate.Queue_sim import Queue_sim
import numpy as np
from simulate.VirtualQueue import VirtualQueue
import time
np.random.seed(0)
task_come = 0.04
tasknum = 0
probable = 0
All_task = []
cluster = Cluster()
taskQueue = Queue_sim()
virtualQueue = VirtualQueue()
Task_list = np.load("/Users/xiangxiangyongan/GitHub/Python/CountLab/simulate/TaskList/TaskLsit_1.npy")
Task_index = 0

def addTask():
    global tasknum
    global probable
    global Task_list
    global Task_index

    if taskQueue.showLen() > 10:
        task_come = 0.05
    elif (taskQueue.showLen() <= 10 and taskQueue.showLen() > 5):
        task_come = 0.07
    else:
        task_come = 0.1

    probable = (probable+np.random.normal())%1.0
    if (probable < task_come):
        task = Task_list[Task_index]
        Task_index += 1
        str = task[0]
        newtask = Task(str)
        newtask.setIndex(int(task[1]),int(task[2]),int(task[3]))
        return newtask
    return -1


def init():
    global taskQueue
    global virtualQueue
    global cluster






def randomGPUTest(task,GPUNUM):
    task.starttime = time.time()
    cluster.putTask(task, GPUNUM)
    taskQueue.deleteTask(task)

def randomTest():
    start_time = time.time()
    while (len(All_task) <200):
        task = addTask()
        if (type(task) != int):
            All_task.append(task)
            taskQueue.addTask(task)
        else:
            pass
        GPUNUM = np.random.choice([1,2,3,4,5,6,7,8])
        # 集群检测是否有任务离开
        uids = cluster.ifEmpty()
        # 检测当前的空闲GPU数目
        num, num_list = cluster.idleGPU()
        if taskQueue.showLen() > 0 and num > GPUNUM:
            randomGPUTest(taskQueue.task_list[0],GPUNUM)
        time.sleep(0.5)





def countUsingTime():
    usingTime = 0
    usingTimeList = []
    waitTime = 0
    waitTimeList = []
    for i in range(150):
        waitTime = waitTime + (All_task[i].startTime - All_task[i].comeTime)*100
        waitTimeList.append((All_task[i].startTime - All_task[i].comeTime)*100)
        usingTime  = usingTime + (All_task[i].endTime - All_task[i].comeTime)*100
        usingTimeList.append((All_task[i].endTime - All_task[i].comeTime)*100)
    np.save("random_wait.npy",waitTimeList)
    np.save("random_using.npy", usingTimeList)
    print("全部任务总用时为{}，任务平均用时为{}".format(int(usingTime),int(usingTime)/150))
    print("任务等待用时为{}，任务平均等待用时为{}".format(int(waitTime),int(waitTime)/150))



if __name__ == '__main__':
    init()
    randomTest()
    countUsingTime()














