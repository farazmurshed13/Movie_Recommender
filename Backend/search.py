import pymongo
import urllib

client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus("7926COAco87") + "@cluster0.zmj8z.mongodb.net/movies?retryWrites=true&w=majority")

db = client['mydatabase']

movies = db['movies']

query = {'original_title': 'Gemini Man', 'country': {"$regex":"\^USA"}}

res = movies.find({'country': "USA"})

print(res[0])