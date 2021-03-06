import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
import sys
import path_eval
import datetime
from math import radians, cos, sin, asin, sqrt, atan2
import urllib.request
import json


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
radius = 0.1
for i in range(df_test.shape[0]):
    path.append({"lat": df_test.iloc[i]['lat'], "lon": df_test.iloc[i]['lon'], "index": i, "time": df_test.iloc[i]['time']})
    x.append(df_test.iloc[i]['lat'])
    y.append(df_test.iloc[i]['lon'])
    names.append(str(i))

ratio = path_eval.path_length_vs_diameter(path)
intersections, intersection_list = path_eval.intersections_count(path)

print("ratio = %6.2f\nintersections = %d" % (ratio, intersections))

def get_street_name_online(lat, lon):
    key2 = "AIzaSyDxxslZEt-75zj2mLR4oXzip4BazkPFHVE"
    google_url = "https://roads.googleapis.com/v1/snapToRoads?path="
    google_url += str(lat)
    google_url += ","
    google_url += str(lon)
    google_url += "&interpolate=false&key=" + key2
    
    bytes_answer = urllib.request.urlopen(google_url).read()
    text_answer = bytes_answer.decode("utf8")
    google_answer = json.JSONDecoder().decode(text_answer)
    
    #print("google answered...")
    
    snapped_lat = google_answer["snappedPoints"][0]["location"]["latitude"]
    snapped_lon = google_answer["snappedPoints"][0]["location"]["longitude"]
    
    snapped_lat = str(snapped_lat)
    snapped_lon = str(snapped_lon)
    
    
    bytes_data = urllib.request.urlopen("https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?prox="+snapped_lat+"%2C"+snapped_lon+"%2C250&mode=retrieveAddresses&maxresults=1&gen=9&app_id=WWBAntTsRvOS0fscgPXJ&app_code=4NuAvXOIiG1gaP_vFTgu5Q").read()

    text_data = bytes_data.decode("utf8")
    here_answer = json.JSONDecoder().decode(text_data)
    
    address = here_answer["Response"]["View"][0]["Result"][0]["Location"]["Address"]
    street = "notReturnedByHere"
    if ("Street" in address):
        street = address["Street"]
    
    #print("here answered...{}".format(address))
    return street

def point_index_in_cluster(lat, lon):
    df_clustered = pd.read_csv('user-location-clustered.csv')
    index = -1

    for i, cluster in enumerate(df_clustered.itertuples()):
        if distance(lat, lon, cluster[1], cluster[2]) < radius:
            return i

    return index

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
    if (point_index_in_cluster(A["lat"], A["lon"]) > -1):
        return False

    B_index = "not_found" # the most recent point older than 15 mins ago
    
    for i in range(len(path) - 2, -1, -1): #reverse loop staring at len(path-2) ending just before -1, with an interation step of -1
        if(time_difference(path[i]["time"], A["time"]) > 15):
            B_index = i
            break  # exit the loop when the first point older than 15 min is found
    
    if B_index == "not_found" :
        return False
  
    for i in range(B_index, len(path) - 1):
        Point = path[i]
        if(distance(Point["lat"], Point["lon"], A["lat"], A["lon"]) > 0.1 or point_index_in_cluster(Point["lat"], Point["lon"]) > -1):
            return False 
            
    return True # if all point are too near send True (is slow)
    
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

last_latitude = path[-1]["lat"]
last_longitude = path[-1]["lon"]

if slow(path):
    print("An alert was sent. Too slow alert. User is now on street {} at latitude {} and longitude {}"
    .format(get_street_name_online(last_latitude, last_longitude), last_latitude, last_longitude))
    show_graph(x, y, names, intersections, ratio) 
    sys.exit(1)

if intersections >= 4:
    print('An alert was sent. The number of intersections is too high ({}). User is now on street {} at latidude {} and longitude {}'
    .format(intersections, get_street_name_online(last_latitude, last_longitude), last_latitude, last_longitude))
    show_graph(x, y, names, intersections, ratio) 
    sys.exit(1)
if ratio > 1.5:
    street_name = get_street_name_online(last_latitude, last_longitude)
    if (street_name == "notReturnedByHere"):
        street_name = "latitude  " + str(last_latitude) + " and longitude  " + str(last_longitude)
        print('An alert was sent. The ratio is too high (%6.2f). User is now at %s.' % (ratio, street_name))
    else:
        print('An alert was sent. The ratio is too high (%6.2f). User is now on street %s at latitude %s and longitude %s.'
         % (ratio, street_name, str(last_latitude), last_longitude))
    show_graph(x, y, names, intersections, ratio) 
    sys.exit(1)


