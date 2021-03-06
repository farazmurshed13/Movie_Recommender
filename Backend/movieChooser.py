import pymongo
import random
import urllib
from heapq import nsmallest
from random import randrange
from decouple import config

MDB_PASS = config('PASS')


# insert genre into the genre graph
def insert(genreGraph, genre, thrill, brainpower, realism, futurism):
    genreGraph[genre] = [thrill,brainpower,realism,futurism]

def insertAllGenre():
    genreGraph = {}
    insert(genreGraph, "Biography", 1, 4, 5, 2)
    insert(genreGraph, "Crime", 5, 4, 4, 3)
    insert(genreGraph, "Drama", 5, 3, 4, 3)
    insert(genreGraph,"History", 1, 4, 5, 1)
    insert(genreGraph,"Adventure", 4, 3, 2, 4)
    insert(genreGraph,"Fantasy", 4, 3, 1, 1)
    insert(genreGraph,"War", 5, 3, 4, 2)
    insert(genreGraph,"Mystery", 4, 5, 3, 3)
    insert(genreGraph,"Horror", 5, 2, 1, 3)
    insert(genreGraph,"Western", 3, 2, 4, 2)
    insert(genreGraph,"Comedy", 3, 1, 4, 3)
    insert(genreGraph,"Family", 3, 1, 4, 3)
    insert(genreGraph,"Action", 5, 2, 2, 4)
    insert(genreGraph,"Sci-fi", 4, 5, 1, 5)
    insert(genreGraph,"Thriller", 5, 4, 3, 3)
    insert(genreGraph,"Sport", 3, 1, 5, 3)
    insert(genreGraph,"Animation", 3, 3, 1, 4)
    insert(genreGraph,"Musical", 3, 1, 3, 3)
    insert(genreGraph,"Film-Noir", 4, 4, 4, 2)
    insert(genreGraph,"Romance", 2, 1, 4, 3)
    return genreGraph
# calculate the k nearest genres
def k_nearest(thrill, brainpower, realism, futurism):
    tempDict = {}
    genreGraph = insertAllGenre()
    for genre in genreGraph:
        genreThrill = genreGraph[genre][0]
        genreBP = genreGraph[genre][1]
        genreRealism = genreGraph[genre][2]
        genreFuturism = genreGraph[genre][3]
        tempDict[genre] = (thrill - genreThrill) ** 2 + (brainpower - genreBP) **2 + \
            (realism - genreRealism) **2 + (futurism - genreFuturism) **2
    return tempDict

# calculate the prob of each genre
def setProbOfEachGenre(diffDict):
    probDict = {}
    res = nsmallest(5, diffDict, key = diffDict.get)
    topFiveSum = 0
    topFiveInverseSum = 0
    for genre in diffDict:
        if genre in res:
            topFiveSum += diffDict[genre]
    for genre in diffDict:
        if genre in res:
            topFiveInverseSum += topFiveSum - diffDict[genre]
    for genre in diffDict:
        if genre in res:
            probability = (topFiveSum - (diffDict[genre]))/(topFiveInverseSum)
            probDict[genre] = probability
        else:
            probDict[genre] = 0
    return probDict
    #pprint(probDict)


# pick a movie

def pickMovie(minRating, minYear, maxYear):
    genreList = random.choices(list(probDict.keys()), weights=probDict.values(), k=3)
    #print(genreList)
    client = pymongo.MongoClient("mongodb+srv://ryan:" + urllib.parse.quote_plus(MDB_PASS) + "@cluster0.zmj8z.mongodb.net/movies?retryWrites=true&w=majority")
    db = client['mydatabase']
    movies = db['movies']
    mydoc = movies.find({ "$and": [{"genre":  {'$regex': '.*' + genreList[0] + '*.'}},{"genre":  {'$regex': '.*' + genreList[1] + '*.'}},
            {"genre":  {'$regex': '.*' + genreList[2] + '*.'}},{"language": "English"},{"avg_vote": {"$gt": int(minRating)}}, 
            {"year": {"$gt": int(minYear), "$lt":int(maxYear)}}]},{"_id":False})
    numDoc = movies.count_documents({ "$and": [{"genre":  {'$regex': '.*' + genreList[0] + '*.'}},{"genre":  {'$regex': '.*' + genreList[1] + '*.'}},
            {"genre":  {'$regex': '.*' + genreList[2] + '*.'}},{"language": "English"},{"avg_vote": {"$gt": int(minRating)}}, 
            {"year": {"$gt": int(minYear), "$lt":int(maxYear)}}]})
    if numDoc == 0:
        return None  
    #randomize index because mongodb has ordering
    randIndex = randrange(0,numDoc)
    index = 0
    for x in mydoc:
        if index == randIndex:
            return x['original_title']

        index +=1
    return None


# generate a list of movies to watch by calling k_nearest and set the probability of each genre
def generateMovList(thrill, brainpower, realism, futurism, minRating, minYear, maxYear):

    # perform k_nearest and prob distrib
    diffDict = k_nearest(thrill, brainpower, realism, futurism)
    setProbOfEachGenre(diffDict)

    it = 0
    while it < 1000 :
        recMovie = pickMovie(minRating,minYear,maxYear)
        if recMovie is None:
            it +=1
            continue
        return recMovie

    return recMovie


#generateMovList(1,4,5,3,"1","1970","2000")
#generateMovList(5,4,2,4,"1","1970","2000")

