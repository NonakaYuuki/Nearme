import numpy as np
import matplotlib.pyplot as plt
import taxi_copy

order=10
excess=1
lack=1/0.4
x=[]
y1=[]
y2=[]
y3=[]
y4=[]
y5=[]

for i in range(100):
    x.append(order+i)
    ave=[]
    for j in range(20):
        if taxi_copy.Simulation(int((order+i)*excess),15,15,int((order+i)*lack),50,j)!=None:
            ave.append(taxi_copy.Simulation(int((order+i)*excess),15,15,int((order+i)*lack),50,j))
    y1.append(np.average(ave))
    y2.append(85+(np.log(order+i))**3)
    y3.append(22+0.8*(np.log(order+i))**3)
    y4.append(23+0.6*(np.log(order+i))**3)
    y5.append(24+0.4*(np.log(order+i))**3)

fig,ax=plt.subplots()
ax.plot(x,y1,color='b',label='Cost')
ax.plot(x,y2,color='r',label='85+(logn)^3')
#ax.plot(x,y3,color='r',label='0.8*log3n')
#ax.plot(x,y4,color='r',label='0.6*log3n')
#ax.plot(x,y5,color='r',label='0.4*log3n')
ax.set_title('(number of taxi) = {0} × (number of order)'.format(int(1/lack)))
ax.set_xlabel('number of taxi')
ax.set_ylabel('Cost')
#ax.set_ylim(50,180)
plt.legend()
plt.show()
