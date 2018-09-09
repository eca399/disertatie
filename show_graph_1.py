import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
import json


with open('transition_mat_with_streets_and_points_and_info.json', 'r') as f:
    transition_mat = json.load(f)
    
kstartPoint = 0
kendPoint = 4
kindex = 1
# import pdb; pdb.set_trace()

x = [elem['lon'] for elem in transition_mat[kstartPoint][kendPoint]['routes'][kindex]['points']]
print(x)
y = [elem['lat'] for elem in transition_mat[kstartPoint][kendPoint]['routes'][kindex]['points']]
print(y)
# oxList
names = [str(elem['index']) for elem in transition_mat[kstartPoint][kendPoint]['routes'][kindex]['points']]

norm = plt.Normalize(1,4)


fig,ax = plt.subplots(figsize=[11, 8])
sc = plt.scatter(x,y,c='b', s=5, norm=norm)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

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

fig.canvas.mpl_connect("motion_notify_event", hover)

#plt.show()
x1, y1 = [44.419223, 44.419514], [26.046114, 26.048614]
# x2, y2 = [1, 10], [3, 2]
no_inters = transition_mat[kstartPoint][kendPoint]['routes'][kindex]['intersections']
ratio = transition_mat[kstartPoint][kendPoint]['routes'][kindex]['ratio'] 
ax.set_title(' of intersections: {} and ratio: {}'.format(no_inters,ratio))
plt.plot(x,y, marker = 'o')
plt.show()