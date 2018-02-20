import wikipedia
import json
from pprint import pprint

cities_data = json.load(open('cities.json'))
event_queries = []

num_queries = 0
count = 0
for city in cities_data:
    print(count)
    count = count + 1
    if count > 300:
        break
    city_name = city["city"]
    city_latitude = city["latitude"]
    city_longitude = city["longitude"]
    # list of quieries in string format
    queries = wikipedia.geosearch(city_latitude, city_longitude, title=None, results=500, radius=10000)
    num_queries = num_queries + len(queries)
print("num quieries = " + str(num_queries))
