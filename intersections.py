import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
import json


with open('transition_mat_with_streets_and_points_and_info.json', 'r') as f:
    transition_mat = json.load(f)

    
df_gps = pd.read_csv('user_location_with_zones.csv')  

df_clustered = pd.read_csv('user-location-clustered.csv')  

with open('Intersections.txt', 'w') as f:
    for i in range(df_clustered.shape[0]):
        for j in range(df_clustered.shape[0]):
            for index in range(len(transition_mat[i][j]['routes'])):
                no_inters = transition_mat[i][j]['routes'][index]['intersections']
                f.write("elem[{}][{}] route[{}] has intersections: {}\n".format(i, j, index, no_inters))