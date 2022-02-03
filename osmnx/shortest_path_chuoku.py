import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from fix_osmnx import re_plot
import shutil

place = {'city' : 'Chuo',
         'state' : 'Tokyo',
         'country' : 'Japan'}
G = ox.graph_from_place(place, network_type="drive")

# impute speed on all edges missing data
G = ox.add_edge_speeds(G)

# calculate travel time (seconds) for all edges
G = ox.add_edge_travel_times(G)

max_node=ox.stats.intersection_count(G,min_streets=1)-1


#ノードのidを返す
def node_id(n):
    return list(G)[n]

#ルート情報を返す関数
def route(orig,dest,time):
    route1 = ox.shortest_path(G, orig, dest, weight="length")
    route1_length_list=ox.utils_graph.get_route_edge_attributes(G, route1, minimize_key="length")
    node_list=[]
    time_list=[]
    length=0
    travel_time=0
    for dic in route1_length_list:
        travel_time+=round(dic['travel_time'],1)
        time_list.append(round(time+travel_time,1))
        length+=dic['length']
    for i in range(len(route1)-1):
        node_list.append(route1[i+1])

    return {'travel_time':travel_time, 'length':length, 'time_list': time_list, 'node_list':node_list}

#アニメーション
def plot(taxi_list,order_list,timespan):
    #animationディレクトリを再生成
    target_dir = './osmnx/animation'
    shutil.rmtree(target_dir)
    os.mkdir(target_dir)

    for t in range(timespan*10+1):
        if t%1000!=0: #コマ数を削る(何秒ごとにするか)
            continue
        route_list=[]
        route_color_list=[]
        for taxi in taxi_list:
            position=taxi.position_list[t]
            route_list.append(ox.shortest_path(G, position, position, weight="length"))
            route_color_list.append('r')
        if order_list[t]!=None:
            for order_child in order_list[t]:
                route_list.append(ox.shortest_path(G, order_child.orig, order_child.dest, weight="length"))
                route_color_list.append('orange')
    
        if len(route_list)>1:
            fig,ax=re_plot.plot_graph_routes(G,route_list,route_colors=route_color_list,node_color='gray',bgcolor='white',edge_color='gray')
        else:
            fig,ax=re_plot.plot_graph_route(G,route_list[0],route_color=route_color_list[0],node_color='gray',bgcolor='white',edge_color='gray')
    
        fig.savefig('./osmnx/animation/t={0}s.png'.format(t+1000000))
        #fig.clf()

from PIL import Image
import os
import glob

# GIFアニメーションを作成
def create_gif(in_dir, out_filename):
    path_list = sorted(glob.glob(os.path.join(*[in_dir, '*']))) # ファイルパスをソートしてリストする
    imgs = [] 
    #print(path_list)                                                  # 画像をappendするための空配列を定義
 
    # ファイルのフルパスからファイル名と拡張子を抽出
    for i in range(len(path_list)):
        img = Image.open(path_list[i])                          # 画像ファイルを1つずつ開く
        imgs.append(img)
    #print(imgs)                                        # 画像をappendで配列に格納していく
 
    # appendした画像配列をGIFにする。durationで持続時間、loopでループ数を指定可能。
    imgs[0].save(out_filename,
                 save_all=True, append_images=imgs[1:], optimize=False, duration=1000, loop=0)