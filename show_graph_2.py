import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
import json
import sys
import path_eval


with open('transition_mat_with_streets_and_points_and_info.json', 'r') as f:
    transition_mat = json.load(f)


fig,ax = plt.subplots(figsize=[11, 8])   
annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))

norm = plt.Normalize(1,4)
cmap = plt.cm.RdYlGn

def get_scatter(x, y):
    sc = plt.scatter(x,y,c='b', s=5, cmap=cmap, norm=norm)
    return sc

# kstartPoint = 0
# kendPoint = 3
# kindex = 0
# x = [elem['lon'] for elem in transition_mat[kstartPoint][kendPoint]['routes'][kindex]['points']]
# print(x)
# y = [elem['lat'] for elem in transition_mat[kstartPoint][kendPoint]['routes'][kindex]['points']]
# print(y)
# names = [str(elem['index']) for elem in transition_mat[kstartPoint][kendPoint]['routes'][kindex]['points']]
if (len(sys.argv) != 2):
    print("example of usage: python main2.py examples/example1.csv")
    sys.exit(1)
examplefile = sys.argv[1]
df_test = pd.read_csv(examplefile)
x = []
y = []
names = []
path = []
for i in range(df_test.shape[0]):
    x.append(df_test.iloc[i]['lat'])
    y.append(df_test.iloc[i]['lon'])
    names.append(str(i))
    path.append({"lat": df_test.iloc[i]['lat'], "lon": df_test.iloc[i]['lon'], "index": i})
sc = get_scatter(x, y)


ratio = path_eval.path_length_vs_diameter(path)
intersections, intersection_list = path_eval.intersections_count(path)
print('intersection_list {}'.format(intersection_list))

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



def show_graph(x, y, names):
    
    annot.set_visible(False)
    fig.canvas.mpl_connect("motion_notify_event", hover)

    #ratio = transition_mat[kstartPoint][kendPoint]['routes'][kindex]['ratio'] 
    ax.set_title('Number of intersections: {} and ratio: {}'.format(intersections, ratio))
    plt.plot(x,y, marker = 'o')
    plt.show()


#show_graph(x, y, names)



print('x {}'.format(x))
print('y {}'.format(y))
print('names {}'.format(names))
show_graph(x, y, names)