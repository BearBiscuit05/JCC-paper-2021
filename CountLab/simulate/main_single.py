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


#对队首任务进行仿真
def LyapunovOpt(task,N):
    lam = task.countFLOPs()
    Z = virtualQueue.task_len
    Q = taskQueue.task_len
    M = task.num
    n = task.epoch
    param = task.param
    BW = cluster.broadWith
    b = task.batchsize #global batchsize
    #比例参数
    V = 6
    min_n = 0
    min_pro = 0
    min_pro_temp = 99999999
    accessGPU = min(task.maxAccessGPU()+1,N+1)
    for i in range(1,accessGPU):
        # if i not in [1,2,4,8]:
        #     continue
        p = cluster.gpu_p(i)

        cost = task.usingTimeCount(p,i,cluster.broadWith)

        profit = V*cost - lam*(Z+5*Q)*(10e-22)
        min_pro_temp = min(profit,min_pro_temp)
        if profit < min_pro :
            min_pro = profit
            min_n = i

    # print("工作量：{}，分配GPU数：{}，GPU功率：{}，带宽：{}，照片数：{}，epoch:{},batchsize:{}".format(lam,min_n,p,BW,M,n,b))
    if min_pro < 0 or accessGPU == task.maxAccessGPU() + 1:
        if min_pro >= 0:
            min_n = task.maxAccessGPU()
        print("[调度决策] task:{},最大可用GPU数目{},当前使用GPU数目:{},耗费时间{},利润为:{}"
              .format(task.uid,accessGPU-1,min_n, cost,min_pro))

        task.starttime = time.time()
        cluster.putTask(task,min_n)
        taskQueue.deleteTask(task)
        if taskQueue.showLen() != 0:
            virtualQueue.addLen(task.countFLOPs())
        else:
            virtualQueue.deleteLen()
    else:
        print("成本太高，不进行决策,此时的最小决策成本为{}".format(min_pro_temp))
        virtualQueue.addLen(0)


def singleGPUTest(task):
    task.starttime = time.time()
    cluster.putTask(task, 1)
    taskQueue.deleteTask(task)

def singleGPUStart():
    start_time = time.time()
    while (len(All_task) <200):
        task = addTask()
        if (type(task) != int):
            All_task.append(task)
            taskQueue.addTask(task)
        else:
            pass
        # 集群检测是否有任务离开
        uids = cluster.ifEmpty()
        # 检测当前的空闲GPU数目
        num, num_list = cluster.idleGPU()
        if taskQueue.showLen() > 0 and num > 0:
            singleGPUTest(taskQueue.task_list[0])
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
    np.save("single_wait.npy",waitTimeList)
    np.save("single_using.npy", usingTimeList)
    print("全部任务总用时为{}，任务平均用时为{}".format(int(usingTime),int(usingTime)/150))
    print("任务等待用时为{}，任务平均等待用时为{}".format(int(waitTime),int(waitTime)/150))



if __name__ == '__main__':
    init()
    singleGPUStart()
    countUsingTime()














