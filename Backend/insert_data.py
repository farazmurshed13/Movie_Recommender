import pymongo
import urllib
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus("7926COAco87") + "@cluster0.zmj8z.mongodb.net/movies?retryWrites=true&w=majority")

db = client['mydatabase']

movies = db['movies']

def csv_to_json(filename, header=None):
    data = pd.read_csv(filename, header=0)
    return data.to_dict('records')

movie_dict = csv_to_json("IMDb_movies.csv")

movies.insert_many(movie_dict)


