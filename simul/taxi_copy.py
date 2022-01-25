# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import copy
import matplotlib.animation as animation
import random


class Taxi:
    def __init__(self,number,position):
        self.position=[position] #タクシーの位置リスト
        self.number=number
        self.status=0 #タクシーがフリーかどうか(フリーの場合は0,迎えの時は1,客乗せて移動中は2)
        self.goal=None #最初は始点の座標が入れられている
        self.real_goal=None #最初に終点の座標が入れられる
    
    def add(self,goal):
        #print(self.posi())
        #print(type(self.posi()))
        way1=Way(self.posi(),self.goal)
        if self.posi()!=goal:
            self.position.append(way1.way())
            #目的地についていた時
            if self.posi()==goal:
                if self.goal==self.real_goal:
                    self.status=0
                else:
                    self.status=2
                    self.goal=self.real_goal
            #print('道順',way1.way())
            #print(self.number,self.status,self.position)

    def add_stay(self):
        #print('stay',self.posi())
        self.position.append(self.posi())
    
        #print(self.number,self.status,self.position)
    
    def posi(self):
        return self.position[len(self.position)-1]

#始点から終点までの道順
class Way:
    def __init__(self,start,goal):
        self.start=start
        self.goal=goal
    
    def way(self):
        if self.goal[0]-self.start[0]>0:
            a=copy.copy(self.start)
            a[0]+=1
            return a
        elif self.goal[0]-self.start[0]<0:
            b=copy.copy(self.start)
            b[0]-=1
            return b
        else:
            if self.goal[1]-self.start[1]>0:
                c=copy.copy(self.start)
                c[1]+=1
                return c
            elif self.goal[1]-self.start[1]<0:
                d=copy.copy(self.start)
                d[1]-=1
                return d

def which_taxi(order,taxi_list): #一番近いタクシーはどれか
    distance_list=[]
    for taxi in taxi_list:
        #print(order[0],taxi.posi())
        distance_list.append(abs(order[0]-taxi.posi()[0])+abs(order[1]-taxi.posi()[1]))
        #print('distance_list',distance_list)
    return [taxi_list[np.argmin(distance_list)],min(distance_list)]

def remove_taxi(taxi_list,taxi_class): #タクシーリストからあるタクシークラスを除く
    for i in taxi_list:
        if i.number==taxi_class.number:
            taxi_list.remove(i)
    return taxi_list


def Simulation(number_of_taxi,x_range,y_range,number_of_order,time_span,seeed):
    #タクシーのオブジェクト生成
    random.seed(seeed)
    taxi_list_c=[]
    for i in range(number_of_taxi):
        taxi_list_c.append(Taxi(i+1,[random.randint(0,x_range),random.randint(0,y_range)]))
    taxi_1=taxi_list_c[0]
    taxi_list=copy.copy(taxi_list_c)

    #注文の生成
    order_list=[]
    order_time=[]
    for i in range(number_of_order):
        order_list.append([[random.randint(0,x_range),random.randint(0,y_range)],[random.randint(0,x_range),random.randint(0,y_range)]])
        order_time.append(random.randint(0,time_span))
        if order_list[len(order_list)-1][0]==order_list[len(order_list)-1][1]:
            #print('この客はなんだ')
            return
    
    #print(order_list)
    #print(order_time)


    #taxi_1=Taxi(1,[1,4])
    #taxi_2=Taxi(2,[2,2])
    #taxi_3=Taxi(3,[4,5]) #addするところ(これを含めて6個ある)
    #taxi_4=Taxi(4,[3,0])
    #taxi_list=[taxi_1,taxi_2,taxi_3,taxi_4] #addするところ

    hold_taxi_list=[]
    order_scatter=[]
    taxi_start_distance=[0]*len(order_time)
    ride_rate_list=[]
    open_list=[] #受け付けられていない注文
    left_order_time=[0]*len(order_time)
    for i in range(time_span): 
        #print('t={0}'.format(i))
        #open_list=[] #order_listの解凍
        for index, j in enumerate(order_time):
            if i==j:
                open_list.append(order_list[index])
        
        order_scatter.append(open_list)

        #乗車率をappend
        count=0
        for taxi in hold_taxi_list:
            if taxi.status==2:
                count+=1
        ride_rate_list.append(float(count)/number_of_taxi) 

        #注文への対応
        open_list_copy=copy.copy(open_list)
        for k in open_list: #注文への対応,迎えにいく
            if taxi_list==[]: #迎えに行けるタクシーが一つもない時
                for order in range(len(order_list)):
                    if k==order_list[order]:
                        left_order_time[order]+=1
                continue
            hold_taxi=which_taxi(k[0],taxi_list)[0]

            for order in range(len(order_time)): #タクシーと客の距離
                if k==order_list[order]:
                    taxi_start_distance[order]=which_taxi(k[0],taxi_list)[1]
            #taxi_start_distance.append(which_taxi(k[0],taxi_list)[1]) #タクシーと客との距離

            hold_taxi_list.append(hold_taxi)
            hold_taxi.status=1
            hold_taxi.goal=k[0]
            hold_taxi.real_goal=k[1]
            remove_taxi(taxi_list,hold_taxi)
            open_list_copy.remove(k)
        open_list=open_list_copy


        
        

        #タクシーの位置の追加   
        for l in taxi_list:
            l.add_stay()
        hold_taxi_list_copy=copy.copy(hold_taxi_list)
        for l in hold_taxi_list_copy:
            l.add(l.goal)
            if l.status==1 and l.goal==l.posi(): #これはタクシーの位置がたまたまお客さんの位置だった時の分岐に使われる！
                l.status=2
                l.goal=l.real_goal
                l.add(l.goal)
            #print(l.status)
            if l.status==0:
                #print(i)
                taxi_list.append(l)
                remove_taxi(hold_taxi_list,l)
        

    order_scatter.append([]) #秒数を合わせる(タクシーの位置リストは0秒から25秒になっているから)
    #for i in taxi_list:
        #print(i.number)
        #print(i.position)
    
    #アニメーション

    #注文を図に表示させるためのリスト
    start_goal_list=[]
    for i in range(len(order_time)):
        start_goal_list1=[[]]*len(taxi_1.position) #[[],[],[]]を作っている
        a=order_list[i]
        distance_order=abs(a[0][0]-a[1][0])+abs(a[0][1]-a[1][1])
        for j in range(taxi_start_distance[i]+distance_order+left_order_time[i]): #(タクシーと客の距離)+(運んでる時間)+(タクシーに無視されてる時間)
            start_goal_list1[j+order_time[i]]=order_list[i]
            #もしも時間内に注文が完了できなかった時
            if j+order_time[i]==len(taxi_1.position)-1:
                break
        start_goal_list.append(start_goal_list1)
    
    #print('Cost={0}'.format(np.average(left_order_time)+np.average(taxi_start_distance)))

    #出力
    return sum(left_order_time)+sum(taxi_start_distance)