#!  conda env
# -*- coding:utf-8 -*-
# Time:2021/4/7 下午9:20
# Author : nishizzma
# File : drawPicture.py

import numpy as np
import matplotlib.pyplot as plt

indexList = [1.0,0.50322,0.25465,0.13365,0.07168,0.04357,0.03167,0.02544,0.02286,0.02154]
batchsize = [np.power(2,i) for i in range(10)]

Alex = [507.7,259.6,133.4,73.4,40,25.8,20.8,17.7,16.7,15.5]
Alex = [1.42*10e+9/Alex[i]  for i in range(len(Alex))]
ResNet = [718.9,359,179.8,92,46.4,29.5,21.9,18.2,16.3,15.9]
ResNet = [1.82*2*10e+9/ResNet[i]  for i in range(len(Alex))]
googlenet = [1610.5,803.6,404.4,206.8,115.5,62.6,38,26,21,19.3]
googlenet = [1.51*2*10e+9/googlenet[i] for i in range(len(Alex))]
print(Alex)
print(ResNet)
print(googlenet)

plt.plot(batchsize,indexList)
plt.plot(batchsize,ResNet,'r')
plt.plot(batchsize,googlenet,'b')

plt.show()


