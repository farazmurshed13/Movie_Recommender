import pymongo
import urllib
from pprint import pprint

client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus("7926COAco87") + "@cluster0.zmj8z.mongodb.net/movies?retryWrites=true&w=majority")

db = client['mydatabase']

movies = db['movies']

query = {'original_title': 'Ip Man', 'country': {"$regex": ".*USA.*"}}

query2 = { '$or' : [ {'title': {'$regex': '.*The Shawshank*.'}}, {'original_title': {'$regex': '.*The Shawshank*.'}}] }


res = movies.find(query2)

pprint(res[0])