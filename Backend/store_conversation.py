import pymongo
import urllib
from random import randint

# set up mongo db client
client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus("7926COAco87") + "@cluster0.zmj8z.mongodb.net/movies?retryWrites=true&w=majority")
db = client['mydatabase']
codes = db['partyCodes']

#
code1 = {
        "code": 1000
        }
codes.insert_one(code1)

# generate party code and store
def generate_code():
    # generate random code in range [0,9999] until unused code is found
    while(True):
        c = randint(0,10000)
        #if
        pass
