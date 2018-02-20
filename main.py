import wikipedia
import json
from pprint import pprint
from multiprocessing.dummy import Pool as ThreadPool
import os.path

cities_data = json.load(open('cities.json'))
cities_data  = cities_data[:900]
event_queries = []


# production settings: results = 1000, count = 900
num_queries = 0
count = 0

final_list = []

# construct files for a city
#for city in cities_data:
def process_city(city):
    # keep track of number of cities being queried
    """
    print("Count: " + str(count))
    count = count + 1
    if count > 900:
        break
        """
    city_name = city["city"]
    city_latitude = city["latitude"]
    city_longitude = city["longitude"]

    # list of quieries in string format
    queries = wikipedia.geosearch(city_latitude, city_longitude, title=None, results=1000, radius=10000)
    # iterate over queries to create individual documents
    for query in queries:
        try:
            file_path = 'documents/' + city_name + '-' + query + '.json'
            query_summary = []
            if os.path.isfile(file_path) == False:
                # get a summary for a query
                query_summary = wikipedia.summary(query, sentences=3, chars=0, auto_suggest=True, redirect=True)

                # create a query and query summary dict
                query_object = {query: query_summary}
                # construct the final document payload
                data = {
                    city_name: query_object
                    }
                # create documents
                city_name = city_name.replace(" ", "_")
                query = query.replace(" ", "_")
                city_name = city_name.replace("/", "_")
                query = query.replace("/", "_")
                f = open(file_path, 'w+')
                json.dump(data, f)
                f.close
                final_list.append(data)
            else:
                print("EXISTS: "+ file_path)
        except:
            print("The following query generated an error: " + query)
    #num_queries = num_queries + len(queries)

# Make the Pool of workers
pool = ThreadPool(10)
# Open the urls in their own threads
# and return the results
results = pool.map(process_city, cities_data)
#close the pool and wait for the work to finish
pool.close()
pool.join()

print("num quieries = " + str(num_queries))
#pprint(final_list)
