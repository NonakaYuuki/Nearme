import numpy as np
import matplotlib.pyplot as plt

#タクシーリスト(active)(初期値)
taxi_list={0:[0,4],1:[2,2]}

#タクシーの位置リスト
taxi_0=[[0,4]]
taxi_1=[[2,2]]

#注文リスト(未完了)([start,goal])
apo_list=[[[2,5],[4,4]],[[1,1],[1,5]]]

#2点の座標からマンハッタン距離を出す(aとbはリスト)
def manha(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

#辞書の逆びき
def inverse(taxi_list,position):
    for k,v in taxi_list.items():
        if position==v:
            return k

#注文の始点から一番近いタクシーはどれか(タクシーの位置を返す)
def neartaxi(start,taxi_list):
    distance_list=[]
    number_list=[]
    for k,v in taxi_list.items():
        distance_list.append(manha(start,v))
        number_list.append(k)
    return number_list[np.argmin(distance_list)]

#2点間の距離の移動時間
def movetime(s,g,v):
    return manha(s,g)/v


print(min([5]))



