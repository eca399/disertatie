# disertatie
existing file:
(user-location.csv)

1)dbscan.py - runs the dbscan, and creates the transition lists and matrix, and plots the graphs
 (transition_mat.json, transition_list.json, sp_trans_list.json, user-location-clustered.csv)
2)processing.py - write in the csv the interest points snap points and streets (user_location_partially_written.csv)
3)google_requsts_urls.py - formats the google requests (google_requests.json)
4)call_google_api.py - calls the google requests (google_answers.json)
5)updating_user_location_with_google_answers.py - adds google answers to the csv (user_location_with_snap_points.csv)
6)here_requests.py - formats and calls the here requests (here_answers.json)
7)updating_user_location_with_here_answers.py - adds here answers to the csv (user_location_with_snap_points_and_streets.csv)
8)adding_streets_to_matrix.py - adds the streets names to the matrix (transition_mat_with_streets.json)
9)interest_point_schedule.py - compute 24 x 7 x 10 matrix schedule (schedule.json)
10)routes_max_times.py - compute the routes max times (routes_max_times.json)
11)interest_points_max_times.py - compute the max times of staying in each interest point (max_times.json)
12)show_graph.py - plots the collected points and the interest points
13)main.py - tests if the user has got lost or confused and sends an alert


main.py

- verifying that the historical maximum of staying in a interest point was not surpassed
- verifying that at the user has been in the current interest point before in history at the same hour and day of the week
- verifying that the current route didn't surpass the maximum historical duration for the current source and destination
- verifying that the current street is found in a historical route from the current source to the current destination
- verifying, in the case when no destination was set, that the current street is found in all historical routes starting at the current source
