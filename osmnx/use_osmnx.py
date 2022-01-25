import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
import folium
import shortest_path_chuoku
import random
import copy

#タクシーオブジェクト
class Taxi:
    def __init__(self, number, position):
        self.position_list=[position] #タクシーが通った交差点のノードリスト
        self.time_list=[0] #各交差点での時間リスト
        self.status_list=[0] #各交差点でのstatusリスト(フリーの場合は0,迎えの時は1,客乗せて移動中は2)
        self.number=number
        self.status=self.status_list[-1] #(フリーの場合は0,迎えの時は1,客乗せて移動中は2)
        self.orig_time=None #始点の座標が入れられている
        self.dest_time=None #終点の座標が入れられる
    
    def add_stay(self):
        self.position_list.append(self.now_position())
    
    def now_position(self):
        return self.position_list[len(self.position_list)-1]

#注文オブジェクト
class Order:
    def __init__(self,number,orig,dest,time):
        self.number=number
        self.orig=orig
        self.dest=dest
        self.time=time

#一番近いタクシーはどれか(タクシーと最短時間を返す)
def which_taxi(order_node,taxi_list,t):
    distance_list=[]
    route_list=[]
    for taxi in taxi_list:
        route1=shortest_path_chuoku.route(taxi.now_position(),order_node,t)
        route_list.append(route1)
        distance_list.append(route1['travel_time'])
    return [taxi_list[np.argmin(distance_list)],min(distance_list),route_list[np.argmin(distance_list)]]

#simulation
def Simulation(number_of_taxi,number_of_order,timespan):
    #タクシーのオブジェクト生成
    random.seed(1)
    taxi_list_c=[]
    for i in range(number_of_taxi):
        taxi_list_c.append(Taxi(i+1,shortest_path_chuoku.node_id(random.randint(0,shortest_path_chuoku.max_node))))
        print('タクシー',taxi_list_c[-1].now_position())
    taxi_1=taxi_list_c[0]
    taxi_list=copy.copy(taxi_list_c)
    
    #注文オブジェクト生成
    random.seed(1)
    order_list=[]
    for i in range(number_of_order):
        order_list.append(Order(i,shortest_path_chuoku.node_id(random.randint(0,shortest_path_chuoku.max_node)),shortest_path_chuoku.node_id(random.randint(0,shortest_path_chuoku.max_node)),random.randint(0,timespan-250)))
        if order_list[-1].orig==order_list[-1].dest:
            print('この客はなんだ')
        print('注文',order_list[-1].orig,order_list[-1].dest,order_list[-1].time)
    
    free_taxi_list=taxi_list
    hold_taxi_list=[]
    order_open_list=[]
    waiting_time_cost=[0]*number_of_order
    taxi_orig_cost=[0]*number_of_order
    orig_dest_cost=[0]*number_of_order
    ride_rate_list=[0]


    #シミュレーション
    for t in range(int(timespan*10)):
        t=round((t+1)*0.1,1)
        #注文リストの解凍
        for order in order_list:
            if order.time==t:
                order_open_list.append(order)
        
        #迎えにいくタクシーを選択
        order_open_list_copy=copy.copy(order_open_list)
        for order in order_open_list:
            if free_taxi_list==[]:
                waiting_time_cost[order.number]+=0.1
            else:
                selected_taxi, time_cost, route_info1=which_taxi(order.orig,free_taxi_list,t)
                route_info2=shortest_path_chuoku.route(order.orig,order.dest,t+route_info1['travel_time'])
                #origに着く時間、destに着く時間の追加
                if time_cost==0:
                    selected_taxi.orig_time=t
                else:
                    selected_taxi.orig_time=route_info1['time_list'][-1]
                selected_taxi.dest_time=route_info2['time_list'][-1]
                #position追加
                selected_taxi.position_list+=route_info1['node_list']
                selected_taxi.position_list+=route_info2['node_list']
                #時間の追加
                selected_taxi.time_list+=route_info1['time_list']
                selected_taxi.time_list+=route_info2['time_list']
                #statusの追加
                selected_taxi.status_list+=[1]*len(route_info1['node_list'])
                selected_taxi.status_list+=[0]*len(route_info2['node_list'])
                #コスト追加
                taxi_orig_cost[order.number]=route_info1['travel_time']
                orig_dest_cost[order.number]=route_info2['travel_time']
                #タクシーをhold_listへ
                free_taxi_list.remove(selected_taxi)
                hold_taxi_list.append(selected_taxi)
                #注文リストから除外
                order_open_list_copy.remove(order)
        order_open_list=order_open_list_copy
        
        #とどまるタクシー
        for taxi in free_taxi_list:
            taxi.add_stay()
            taxi.time_list.append(t)
            taxi.status_list.append(0)
        
        # hold_listのタクシーの position,timeの間埋め
        for taxi in hold_taxi_list:
            if round(taxi.time_list[int(t*10)]-taxi.time_list[int(t*10)-1],1)!=0.1:
                taxi.time_list.insert(int(t*10),t)
                taxi.position_list.insert(int(t*10)-1,taxi.position_list[int(t*10)-1])
                taxi.status_list.insert(int(t*10)-1,taxi.position_list[int(t*10)-1])

        
        #タクシーの解放 & 乗車率
        count=0
        hold_taxi_list_copy=copy.copy(hold_taxi_list)
        for taxi in hold_taxi_list:
            if taxi.dest_time==t:
                hold_taxi_list_copy.remove(taxi)
                free_taxi_list.append(taxi)
            elif taxi.status==2:
                count+=1
        ride_rate_list.append(float(count)/number_of_taxi)
        hold_taxi_list=hold_taxi_list_copy
    #print(taxi_1.position_list)
    #print(taxi_1.time_list)
    #print(route_info1['time_list'])
    #print(route_info2['time_list'])
    #for i in range(len(taxi.time_list)-1):
        #if round(taxi.time_list[i+1]-taxi.time_list[i],1)!=0.1:
            #print('kora',i)
    
    #アニメーション
    

if __name__=='__main__':
    Simulation(1,1,500)

