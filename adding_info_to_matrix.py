import pandas as pd
import json

import path_eval


with open('transition_mat_with_streets_and_points.json', 'r') as f:
    transition_mat = json.load(f)

with open('transition_list.json', 'r') as f:
    transition_list = json.load(f)
   
with open('sp_trans_list.json', 'r') as f:
    sp_trans_list = json.load(f)
    
with open('interest_points.json', 'r') as f:
    interest_points = json.load(f)
    
df_gps = pd.read_csv('user_location_partially_written.csv')  

df_clustered = pd.read_csv('user-location-clustered.csv')  


number_of_clusters = len(df_clustered)

for i in range(number_of_clusters):
    for j in range(number_of_clusters):
        routes = transition_mat[i][j]["routes"]
        for route in routes:
            points = route["points"]
            route["ratio"] = path_eval.path_length_vs_diameter(points)
            route["intersections"] = path_eval.intersections_count(points)
            
with open('transition_mat_with_streets_and_points_and_info.json', 'w') as outfile:
    json.dump(transition_mat, outfile)
