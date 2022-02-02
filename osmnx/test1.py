import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
from fix_osmnx import re_plot

place = {'city' : 'Chuo',
         'state' : 'Tokyo',
         'country' : 'Japan'}
G = ox.graph_from_place(place, network_type="drive")
# impute speed on all edges missing data
G = ox.add_edge_speeds(G)

# calculate travel time (seconds) for all edges
G = ox.add_edge_travel_times(G)
route1 = ox.shortest_path(G, 5929256269, 588385246, weight="length")
route2 = ox.shortest_path(G, 1130812252, 260426062, weight="length")

route1_length_list=ox.utils_graph.get_route_edge_attributes(G, route1, minimize_key="length")
time_list=[]
length=0
travel_time=0

for dic in route1_length_list:
    
    travel_time+=round(dic['travel_time'],1)
    length+=dic['length']
    #print(dic['speed_kph'])
#print(length)
#print(travel_time)

route2_length_list=ox.utils_graph.get_route_edge_attributes(G, route2, minimize_key="length")
time_list=[]
length=0
travel_time=0
for dic in route2_length_list:
    travel_time+=round(dic['travel_time'],1)
    length+=dic['length']
    #print(dic['speed_kph'])
#print(length)
#print(travel_time)
#print(route1_length_list)
#print(route2_length_list)

#artists=[]
fig,ax=re_plot.plot_graph_route(G,route1,route_color='r',node_color='dimgray',bgcolor='white',edge_color='dimgray')
fig.savefig('./osmnx/test.png')

fig,ax=re_plot.plot_graph_route(G,route2,route_color='r',node_color='black',bgcolor='white',edge_color='black')

