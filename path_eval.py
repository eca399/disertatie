import math
from math import radians, cos, sin, asin, sqrt, atan2

def distance(a, b):
    return math.sqrt((a["lat"]-b["lat"])**2 + (a["lon"]-b["lon"])**2)

def distance2(lat1, lon1, lat2, lon2):
    radius = 6371.0088 # km in one radian

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = radius * c
    
    return d

def path_length_vs_diameter(path):
    path_length = 0
  
    for i in range(len(path) - 1):
        a = path[i]
        b = path[i+1]
        path_length += distance(a, b)
    
    max_distance = 0
    
    for a in path:
        for b in path:
            ab = distance(a, b)
            if(max_distance < ab):
                max_distance = ab
         
    print('path length {} and max distance {}'.format(path_length, max_distance))
    return path_length/max_distance

#print(path_length_vs_diameter([{"lat":10, "lon":10},{"lat":10, "lon":110},{"lat":110, "lon":110}]))

def intersections_count(path):
    result = 0
    min_segment_len = 0.08
    intersection_list = []
    for i in range(len(path) - 2):
        a = path[i]
        b = path[i + 1]
        for j in range(i + 2, len(path) - 1):
            m = path[j]
            n = path[j + 1]
        
            
            if(intersects2(a, b, m, n)) and distance2(a["lat"], a["lon"], b["lat"], b["lon"]) > min_segment_len and \
            distance2(m["lat"], m["lon"], n["lat"], n["lon"]) > min_segment_len:

                intersection_list.append([i, i + 1, j, j + 1])
                result += 1
                
    return result, intersection_list

def ccw(A,B,C):
    return (C["lat"]-A["lat"]) * (B["lon"]-A["lon"]) > (B["lat"]-A["lat"]) * (C["lon"]-A["lon"])

# Return true if line segments AB and CD intersect
def intersects2(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)