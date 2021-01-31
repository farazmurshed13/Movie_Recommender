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
                "num_users" : 0,
                "users_done": 0,
                "min_date" : "",
                "max_date" : "",
                "min_rating" : ""
            }
            codes.insert_one(new_code)
            break
    return c

# store initial host webpage info (num users, date range, rating)
def host_submit(dic, c):
    client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus(
        "7926COAco87") + "@cluster0.zmj8z.mongodb.net/mydatabase?retryWrites=true&w=majority")
    db = client['mydatabase']
    codes = db['partyCodes']
    codes.update_one({"code": c}, {"$set": {"num_users": dic['numwatchers'], "min_date": dic['mindate'], "max_date": dic['maxdate'], "min_rating": dic['minrating'] } } )


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

# return True if all users done
def done(c):
    client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus(
        "7926COAco87") + "@cluster0.zmj8z.mongodb.net/mydatabase?retryWrites=true&w=majority")
    db = client['mydatabase']
    codes = db['partyCodes']

    codes.update_one( {"code" : c}, { "$inc" : {"users_done" : 1}} )

    # check if all users done
    ud = codes.find({"code": c}, {"users_done": 1, "_id": 0})
    for i in ud:
        n_ud = i["users_done"]
    nu = codes.find({"code": c}, {"num_users": 1, "_id": 0})
    for j in nu:
        n_nu = j["num_users"]

    return n_ud == n_nu

# get array of total responses
def get_tot_resp(c):
    client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus(
        "7926COAco87") + "@cluster0.zmj8z.mongodb.net/mydatabase?retryWrites=true&w=majority")
    db = client['mydatabase']
    codes = db['partyCodes']

    # get Qs
    loc1 = codes.find({"code": c}, {"1": 1, "_id": 0})
    for i in loc1:
        q1 = i["1"]
    loc2 = codes.find({"code": c}, {"2": 1, "_id": 0})
    for j in loc2:
        q2 = j["2"]
    loc3 = codes.find({"code": c}, {"3": 1, "_id": 0})
    for k in loc3:
        q3 = k["3"]
    loc4 = codes.find({"code": c}, {"4": 1, "_id": 0})
    for g in loc4:
        q4 = j["4"]

    # get other necessary data
    loc5 = codes.find({"code": c}, {"1": 1, "_id": 0})
    for i in loc5:
        min_rat = i["1"]
    loc6 = codes.find({"code": c}, {"2": 1, "_id": 0})
    for j in loc6:
        min_dat = j["2"]
    loc7 = codes.find({"code": c}, {"3": 1, "_id": 0})
    for k in loc7:
        max_dat = k["3"]

    return [q1, q2, q3, q4, min_rat, min_dat, max_dat]