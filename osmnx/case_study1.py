import numpy as np
import use_osmnx
import matplotlib.pyplot as plt
import os

#タクシーの数がどれくらいで待ち時間がどのくらいになるか

minimum_taxi=1
max_taxi=10
number_of_order=3
timespan=3600
max_wait_time_list=[]
ave_wait_time_list=[]
taxi_number_list=[]
x=[i for i in range(number_of_order)]
os.mkdir('./osmnx/result/order/{}order'.format(number_of_order))
for i in range(minimum_taxi,max_taxi+1):
    if i%3!=1:
        continue
    print(i)
    #それぞれのタクシー数でのwait_timeの分散を見たい
    wait_time_list=[c/60 for c in use_osmnx.Simulation(i,number_of_order,timespan,graph=False,animation=False)['cost_list']]
    plt.bar(x,wait_time_list)
    plt.title('number of order = {}'.format(number_of_order))
    plt.xlabel('order')
    plt.ylabel('waiting time [min]')
    plt.savefig('./osmnx/result/order/{0}order/{1}taxi_{2}order_per_1h.png'.format(number_of_order,i,number_of_order))
    plt.clf()
    max_wait_time_list.append(max(wait_time_list))
    ave_wait_time_list.append(np.average(wait_time_list))
    taxi_number_list.append('{}'.format(i%10))

print(taxi_number_list)
print(max_wait_time_list)
#グラフ化
plt.bar(taxi_number_list,max_wait_time_list)
plt.title('number of order = {}'.format(number_of_order))
plt.xlabel('Number of taxi')
plt.ylabel('Max waiting time [min]')
plt.savefig('./osmnx/result/max/{0}taxi_{1}order_per_1h.png'.format(max_taxi,number_of_order))
#plt.show()
plt.clf()
plt.bar(taxi_number_list,ave_wait_time_list)
plt.title('number of order = {}'.format(number_of_order))
plt.xlabel('Number of taxi')
plt.ylabel('Average waiting time [min]')
plt.savefig('./osmnx/result/average/{0}taxi_{1}order_per_1h.png'.format(max_taxi,number_of_order))


