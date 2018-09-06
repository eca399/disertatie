import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
import json


with open('transition_mat_with_streets_and_points_and_info.json', 'r') as f:
    transition_mat = json.load(f)

with open('transition_list.json', 'r') as f:
    transition_list = json.load(f)
   
with open('sp_trans_list.json', 'r') as f:
    sp_trans_list = json.load(f)
    
with open('interest_points.json', 'r') as f:
    interest_points = json.load(f)
    
df_gps = pd.read_csv('user_location_with_zones.csv')  

df_clustered = pd.read_csv('user-location-clustered.csv')  

kstartPoint = 0
kendPoint = 1
kindex = 0
# import pdb; pdb.set_trace()
oxList = [elem['lat'] for elem in transition_mat[kstartPoint][kendPoint]['routes'][kindex]['points']]
print(oxList)
oYList = [elem['lon'] for elem in transition_mat[kstartPoint][kendPoint]['routes'][kindex]['points']]
print(oYList)
# oxList

fig, ax = plt.subplots(figsize=[11, 8])
# rs_scatter = ax.scatter(oxList, oYList, c='m', edgecolor='None', alpha=0.3, s=120)
df_scatter = ax.scatter(oxList, oYList, c='k', alpha=0.5, s=3)
ax.set_title('Full data set vs DBSCAN reduced set')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend([df_scatter], ['GPS Points'], loc='upper left')
plt.show()
