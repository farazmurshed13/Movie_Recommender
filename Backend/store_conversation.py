import pymongo
import urllib
from random import randint

# generate party code and store for first user
def generate_code():
    client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus("7926COAco87") + "@cluster0.zmj8z.mongodb.net/mydatabase?retryWrites=true&w=majority")
    db = client['mydatabase']
    codes = db['partyCodes']
    # generate random code in range [0,9999] until unused code is found
    c = 0
    while(True):
        c = randint(0,10000)
        if codes.count_documents({"code" : c}, limit=1) == 0:
            # unused code found
            new_code = {
                "code": c,
                "1" : 0,
                "2" : 0,
                "3" : 0,
                "4": 0,
                "users_list" : [],
                "users_done": 0
            }
            codes.insert_one(new_code)
            break
    return c

# verify party code
def verify_party(pc):
    client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus("7926COAco87") + "@cluster0.zmj8z.mongodb.net/mydatabase?retryWrites=true&w=majority")
    db = client['mydatabase']
    codes = db['partyCodes']

    if codes.count_documents({"code": pc}, limit=1) == 1:
        return True
    else:
        return False

# update question responses in database
def record_response(q, resp, c):
    client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus(
        "7926COAco87") + "@cluster0.zmj8z.mongodb.net/mydatabase?retryWrites=true&w=majority")
    db = client['mydatabase']
    codes = db['partyCodes']
    codes.update_one( {"code" : c}, { "$inc" : {q : resp}} )

# add a member to party code
def add_member(member, c):
    client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus(
        "7926COAco87") + "@cluster0.zmj8z.mongodb.net/mydatabase?retryWrites=true&w=majority")
    db = client['mydatabase']
    codes = db['partyCodes']
    codes.update_one({"code": c}, {"$push": {"users_list" : member}})

# get code for member
def get_code(member):
    client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus(
        "7926COAco87") + "@cluster0.zmj8z.mongodb.net/mydatabase?retryWrites=true&w=majority")
    db = client['mydatabase']
    codes = db['partyCodes']
    found = codes.find({"users_list" : member }, {"code" : 1, "_id" : 0})
    for i in found:
        return i["code"]


add_member("+1929", 5749)
print(get_code("+1921"))