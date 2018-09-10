import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
import sys
import path_eval
import datetime
from math import radians, cos, sin, asin, sqrt, atan2
# from show_graph_2 import *


if (len(sys.argv) != 2):
    print("example of usage: python main2.py examples/example1.csv")
    sys.exit(1)

examplefile = sys.argv[1]
df_test = pd.read_csv(examplefile)







path = []
x = []
y = []
names = []
path = []
for i in range(df_test.shape[0]):
    path.append({"lat": df_test.iloc[i]['lat'], "lon": df_test.iloc[i]['lon'], "index": i, "time": df_test.iloc[i]['time']})
    x.append(df_test.iloc[i]['lat'])
    y.append(df_test.iloc[i]['lon'])
    names.append(str(i))

def time_difference(date_time1, date_time2):
    d1 = datetime.datetime.strptime(date_time1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(date_time2, '%Y-%m-%d %H:%M:%S')
    return (d2 - d1).total_seconds() / 60

def distance(lat1, lon1, lat2, lon2):
    radius = 6371.0088 # km in one radian

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = radius * c
    
    return d    
    
def slow(path):

    A = path[-1] #current point is the last point in path

    B_index = "not_found" # the most recent point older than 20 mins ago
    
    for i in range(len(path) - 2, -1, -1): #reverse loop staring at len(path-2) ending just before -1, with an interation step of -1
        if(time_difference(path[i]["time"], A["time"]) > 20):
            B_index = i
            break  # exit the loop when the first point older than 20 min is found
            
  
    result = False
    
    if B_index == "not_found" :
        return False
  
    result = True
    for i in range(B_index, len(path) - 1):
        Point = path[i]
        if(distance(Point["lat"], Point["lon"], A["lat"], A["lon"]) > 0.1):
            result = False # if all point are too near send True (is slow)
            
    return result
    

if slow(path):
    print("Sending too slow alert")

    
ratio = path_eval.path_length_vs_diameter(path)
intersections, intersection_list = path_eval.intersections_count(path)

print("ratio = {}\nintersections = {}".format(ratio, intersections))

if intersections > 15 or ratio > 1.5:
    print('An alarm was sent')
###plot the graph
fig,ax = plt.subplots(figsize=[11, 8])   
annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))

norm = plt.Normalize(1,4)

def get_scatter(x, y):
    sc = plt.scatter(x,y,c='b', s=5, norm=norm)
    return sc
sc = get_scatter(x, y)

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}".format(" ".join([names[n] for n in ind["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor('b')
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()



def show_graph(x, y, names, numb_intersections, ratio):
    
    annot.set_visible(False)
    fig.canvas.mpl_connect("motion_notify_event", hover)

    #ratio = transition_mat[kstartPoint][kendPoint]['routes'][kindex]['ratio'] 
    ax.set_title('Number of intersections: {} and ratio: {}'.format(numb_intersections, ratio))
    plt.plot(x,y, marker = 'o')
    plt.show()

show_graph(x, y, names, intersections, ratio)  
