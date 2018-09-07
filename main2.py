import pandas as pd
import sys
import path_eval


if (len(sys.argv) != 2):
    print("example of usage: python main.py examples/example1.csv")
    sys.exit(1)

examplefile = sys.argv[1]


df_test = pd.read_csv(examplefile)

path = []
for i in range(df_test.shape[0]):
    path.append({"lat": df_test.iloc[i]['lat'], "lon": df_test.iloc[i]['lon'], "index": i})
    

ratio = path_eval.path_length_vs_diameter(path)
intersections = path_eval.intersections_count(path)

print("ratio = {}\nintersections = {}".format(ratio, intersections))

    