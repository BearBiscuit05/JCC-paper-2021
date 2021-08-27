# Author : nishizzma
# File : 1.py
import numpy as np
import matplotlib.pyplot as plt

#定义x、y散点坐标
x = [1,2,4,8,16,32,64,128,256,512]
x = np.array(x)
print('x is :\n',x)
time = [507.7,259.6,133.4,73.4,40,25.8,20.8,17.7,16.7,15.5]
FLOPs = 0.71*2*6000
num = []
for i in range(len(x)):
    num.append(FLOPs/time[i])
#num = [16781563,32819722,63868065,116076294,213000000,330232558,409615384,481355932,510179640,549677419]
y = np.array(num)
print('y is :\n',y)
#用3次多项式拟合
f1 = np.polyfit(x, y, 4)
print('f1 is :\n',f1)
p1 = np.poly1d(f1)
print('p1 is :\n',p1)
#也可使用yvals=np.polyval(f1, x)
yvals = p1(x)#拟合y值
print('yvals is :\n',yvals)
#绘图
plot1 = plt.plot(x, y, 's',label='original values')
plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc=4) #指定legend的位置右下角
plt.title('polyfitting')
plt.show()
