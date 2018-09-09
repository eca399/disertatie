import math

def distance(a, b):
    return math.sqrt((a["lat"]-b["lat"])**2 + (a["lon"]-b["lon"])**2)

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
         
    return path_length/max_distance

#print(path_length_vs_diameter([{"lat":10, "lon":10},{"lat":10, "lon":110},{"lat":110, "lon":110}]))



def intersections_count(path):
    result = 0
    intersection_list = []
    for i in range(len(path) - 2):
        a = path[i]
        b = path[i + 1]
        for j in range(i + 2, len(path) - 1):
            m = path[j]
            n = path[j + 1]
            
#            if(intersects2(a,b,m,n) != intersects(a,b,m,n)):
#               print("diff")
            
            if(intersects2(a, b, m, n)):
                intersection_list.append([i, i + 1, j, j + 1])
                result += 1
                
    return result, intersection_list

#tests if segment (a,b) intersects segment (m,n)
def intersects(a, b, m, n):
    X1 = a["lon"]
    Y1 = a["lat"]
    X2 = b["lon"]
    Y2 = b["lat"]
    X3 = m["lon"]
    Y3 = m["lat"]
    X4 = n["lon"]
    Y4 = n["lat"]
    
    I1 = [min(X1,X2), max(X1,X2)]
    I2 = [min(X3,X4), max(X3,X4)]
    
      
    if (max(X1,X2) < min(X3,X4)):
        return False
        
    if (X1 == X2 or X3 == X4):
        return True
        
    A1 = (Y1-Y2)/(X1-X2)
    A2 = (Y3-Y4)/(X3-X4)
    b1 = Y1-A1*X1
    b2 = Y3-A2*X3
    
    if (A1 == A2):
        return False
        
    Xa = (b2 - b1) / (A1 - A2)
    
    if((Xa < max(min(X1,X2), min(X3,X4))) or (Xa > min(max(X1,X2), max(X3,X4)))):
       return False
    else:
       return True
    

#print(intersections_count([{"lat":0, "lon":0},{"lat":0, "lon":100},{"lat":100, "lon":100}, {"lat":-5, "lon":50}]))


def ccw(A,B,C):
    return (C["lat"]-A["lat"]) * (B["lon"]-A["lon"]) > (B["lat"]-A["lat"]) * (C["lon"]-A["lon"])

# Return true if line segments AB and CD intersect
def intersects2(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)