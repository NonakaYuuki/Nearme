import numpy as np
import osmnx as ox
import folium
import networkx as nx

place = {'city' : 'Chuo',
         'state' : 'Tokyo',
         'country' : 'Japan'}
G = ox.graph_from_place(place, network_type="drive")


# impute speed on all edges missing data
G = ox.add_edge_speeds(G)

# calculate travel time (seconds) for all edges
G = ox.add_edge_travel_times(G)

hwy_speeds = {"residential": 35, "secondary": 50, "tertiary": 60}
G = ox.add_edge_speeds(G, hwy_speeds)
G = ox.add_edge_travel_times(G)

# calculate two routes by minimizing travel distance vs travel time
orig = list(G)[120]
dest = list(G)[1]
#orig=1443467259
#dest=1054155212
route1 = ox.shortest_path(G, orig, dest, weight="length")
route2 = ox.shortest_path(G, orig, dest, weight="travel_time")
#print(list(G))
print(orig)
print(dest)
#print(route1)
# compare the two routes
route1_length_list=ox.utils_graph.get_route_edge_attributes(G, route1, minimize_key="length")
route2_length_list=ox.utils_graph.get_route_edge_attributes(G, route2, minimize_key="length")
route1_time_list=ox.utils_graph.get_route_edge_attributes(G, route1, minimize_key="travel_time")
route2_time_list=ox.utils_graph.get_route_edge_attributes(G, route2, minimize_key="travel_time")

route1_length=0
route2_length=0
route1_time=0
route2_time=0
print(len(route1_length_list))
print(len(route1))
for i in route1_length_list:
    route1_length+=i['length']
    route1_time+=round(i['travel_time'])
for i in route2_length_list:
    route2_length+=i['length']
    route2_time+=round(i['travel_time'])


#route1_length = int(sum(ox.utils_graph.get_route_edge_attributes(G, route1, minimize_key="length")))
#route2_length = int(sum(ox.utils_graph.get_route_edge_attributes(G, route2, minimize_key="length")))
#route1_time = int(sum(ox.utils_graph.get_route_edge_attributes(G, route1, minimize_key="travel_time")))
#route2_time = int(sum(ox.utils_graph.get_route_edge_attributes(G, route2, minimize_key="travel_time")))
print("Route 1 is", route1_length, "meters and takes", route1_time, "seconds.")
print("Route 2 is", route2_length, "meters and takes", route2_time, "seconds.")
outfile = "result.png"
opts = {"node_size": 5, "bgcolor": "white", "node_color": "blue", "edge_color": "blue"}
ox.plot_graph_routes(G, [route1,route2], show=False, save=True, filepath=outfile, **opts)
ox.plot_graph_route(G, [list(G)[1]], show=False, save=True, filepath='result1.png', **opts)