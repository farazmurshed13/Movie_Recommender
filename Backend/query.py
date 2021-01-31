import pymongo
from pprint import pprint
client = pymongo.MongoClient("mongodb+srv://ryan:" + 
        urllib.parse.quote_plus("7926COAco87") + "@cluster0.zmj8z.mongodb.net/movies?retryWrites=true&w=majority")
db = client['mydatabase']

movies = db['movies']

mydoc = movies.find({},{ "genre":1, "_id":False})
mySet = set()

for x in mydoc:
    splitStr = x['genre'].split()
    for genre in splitStr:
        genre = genre.replace(',','')
        if genre in mySet:
            continue
        print(genre)
        mySet.add(genre)
print(len(mySet))