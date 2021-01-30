import pymongo
client = pymongo.MongoClient("mongodb+srv://articbear1999:Jacoblin1!@cluster0.zmj8z.mongodb.net/movies?retryWrites=true&w=majority")
db = client['mydatabase']

movies = db['movies']

myquery = { "title": "Miss Jerry" }

mydoc = movies.find(myquery)

for x in mydoc:
  print(x) 