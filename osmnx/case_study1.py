import numpy as np
import use_osmnx
import matplotlib.pyplot as plt

#タクシーの数がどれくらいで待ち時間がどのくらいになるか

minimum_taxi=1
max_taxi=40
number_of_order=30
timespan=3600
max_wait_time_list=[]
taxi_number_list=[]

for i in range(minimum_taxi,max_taxi+1):
    max_wait_time_list.append(max(use_osmnx.Simulation(i,number_of_order,timespan,graph=False,animation=False)['cost_list'])/60)
    taxi_number_list.append('{}'.format(i))

print(taxi_number_list)
print(max_wait_time_list)
#グラフ化
plt.bar(taxi_number_list,max_wait_time_list)
plt.title('number of order = {}'.format(number_of_order))
plt.xlabel('Number of taxi')
plt.ylabel('Max waiting time [min]')
plt.show()


