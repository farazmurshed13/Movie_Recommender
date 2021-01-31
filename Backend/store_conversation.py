import pymongo
import urllib
from random import randint

# set up mongo db client


# generate party code and store for first user
def generate_code():
    client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus("7926COAco87") + "@cluster0.zmj8z.mongodb.net/mydatabase?retryWrites=true&w=majority")
    db = client['mydatabase']
    codes = db['partyCodes']
    # generate random code in range [0,9999] until unused code is found
    while(True):
        c = randint(0,10000)
        if codes.count_documents({"code" : c}, limit=1) == 0:
            # unused code found
            new_code = {
                "code": c,
                "q1": 0,
                "q2": 0,
                "q3": 0,
                "q4": 0
            }
            codes.insert_one(new_code)
            break

#verify party code
def verify_party(pc):
    if pc == 829:
        return True
    else:
        return False

    # client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus(
    #     "7926COAco87") + "@cluster0.zmj8z.mongodb.net/mydatabase?retryWrites=true&w=majority")
    # db = client['mydatabase']
    # codes = db['partyCodes']

    # if codes.count_documents({"code": pc}, limit=1) == 1:
    #     return True
    # else:
    #     return False
