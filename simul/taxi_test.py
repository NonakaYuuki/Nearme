import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

#軸の最小値、最大値
dRange = [0.0 , 1.0]

if __name__ == "__main__":
    #グラフ 散布図
    fig_scatter = plt.figure()
    plt_scatter = []

    # 実行
    for count  in  range(30):
        #グラフ 散布図
        x_1 = []
        x_2 = []
        for n in range(50):
            x_1.append(np.random.rand())
            x_2.append(np.random.rand())

        x_scatter = plt.scatter(x_1, x_2 , c="blue")

        x_scatter_red  = plt.scatter(np.random.rand(), 
                                     np.random.rand(),
                                     c="red",
                                     marker="*",
                                     s=200)
        # タイトルテキスト
        title = plt.text((dRange[0]+dRange[1]) /2 , dRange[1], 
                         'Count={:d}'.format(count),
                         ha='center', va='bottom',fontsize='large')

        plt_scatter.append([x_scatter,x_scatter_red,title])


    #散布図
    # アニメーション作成
    plt.xlim(dRange[0],dRange[1])
    plt.ylim(dRange[0],dRange[1])
    plt.grid(True)

    ani = animation.ArtistAnimation(fig_scatter, plt_scatter, interval=500)
    plt.show()