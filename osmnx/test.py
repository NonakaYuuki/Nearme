import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
place = {'city' : 'Chuo',
         'state' : 'Tokyo',
         'country' : 'Japan'}
#G = ox.graph_from_place(place, network_type="drive")
#route1 = ox.shortest_path(G, list(G)[2], list(G)[2], weight="travel_time")
#route2 = ox.shortest_path(G, list(G)[4], list(G)[4], weight="travel_time")

#artists=[]
#fig,ax=ox.plot.plot_graph_route(G,route2,route_color='r',node_color='g',bgcolor='white',edge_color='g')
#fig.savefig('./osmnx/animation/anim.png')

#fig,ax=ox.plot.plot_graph_route(G,route2,route_color='r',node_color='g',bgcolor='white',edge_color='g')
#plt.show()




from PIL import Image
import os
import glob

# GIFアニメーションを作成
def create_gif(in_dir, out_filename):
    path_list = sorted(glob.glob(os.path.join(*[in_dir, '*']))) # ファイルパスをソートしてリストする

    #print(path_list)
    imgs = []                                                   # 画像をappendするための空配列を定
# ファイルのフルパスからファイル名と拡張子を抽出
    for i in range(len(path_list)):
        img = Image.open(path_list[i])                          # 画像ファイルを1つずつ開く
        imgs.append(img)
    #print(imgs)                                        # 画像をappendで配列に格納していく
 
    # appendした画像配列をGIFにする。durationで持続時間、loopでループ数を指定可能。
    imgs[0].save(out_filename,
                 save_all=True, append_images=imgs[1:], optimize=False, duration=30, loop=0)


 
# GIFアニメーションを作成する関数を実行する
if __name__=='__main__':
    create_gif(in_dir='animation', out_filename='animation.gif')


