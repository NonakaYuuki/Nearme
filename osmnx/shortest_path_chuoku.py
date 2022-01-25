import osmnx as ox
import numpy as np

place = {'city' : 'Chuo',
         'state' : 'Tokyo',
         'country' : 'Japan'}
G = ox.graph_from_place(place, network_type="drive")

# impute speed on all edges missing data
G = ox.add_edge_speeds(G)

# calculate travel time (seconds) for all edges
G = ox.add_edge_travel_times(G)

max_node=120


#ノードのidを返す
def node_id(n):
    return list(G)[n]

#ルート情報を返す関数
def route(orig,dest,time):
    route1 = ox.shortest_path(G, orig, dest, weight="travel_time")
    route1_length_list=ox.utils_graph.get_route_edge_attributes(G, route1, minimize_key="travel_time")
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
