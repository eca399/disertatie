import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
import sys
import path_eval
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
    path.append({"lat": df_test.iloc[i]['lat'], "lon": df_test.iloc[i]['lon'], "index": i})
    x.append(df_test.iloc[i]['lat'])
    y.append(df_test.iloc[i]['lon'])
    names.append(str(i))
    
ratio = path_eval.path_length_vs_diameter(path)
intersections, intersection_list = path_eval.intersections_count(path)

print("ratio = {}\nintersections = {}".format(ratio, intersections))
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