import pymongo
import numpy as np
import random
from pprint import pprint
from heapq import nsmallest 
from random import randrange
genreGraph = {}
diffDict = {}
probDict = {}
movieList = []
#insert genre into the genre graph
def insert(genre, thrill, brainpower, realism, futurism):
    genreGraph[genre] = [thrill,brainpower,realism,futurism]

# calculate the k closest genres
def kClosest(thrill, brainpower, realism, futurism):
    tempDict = {}
    for genre in genreGraph:
        genreThrill = genreGraph[genre][0]
        genreBP = genreGraph[genre][1]
        genreRealism = genreGraph[genre][2]
        genreFuturism = genreGraph[genre][3]
        tempDict[genre] = (thrill - genreThrill) ** 2 + (brainpower - genreBP) **2 + \
            (realism - genreRealism) **2 + (futurism - genreFuturism) **2
    return tempDict

# calculate the prob of each genre
def setProbOfEachGenre():
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
    #pprint(probDict)


#pick a movie
def pickMovie(recMovieList, minRating, minYear, maxYear):
    genreList = random.choices(list(probDict.keys()), weights=probDict.values(), k=3)
    #print(genreList)
    client = pymongo.MongoClient("mongodb+srv://articbear1999:Jacoblin1!@cluster0.zmj8z.mongodb.net/movies?retryWrites=true&w=majority")
    db = client['mydatabase']
    movies = db['movies']
    mydoc = movies.find({ "$and": [{"genre":  {'$regex': '.*' + genreList[0] + '*.'}},{"genre":  {'$regex': '.*' + genreList[1] + '*.'}},
            {"genre":  {'$regex': '.*' + genreList[2] + '*.'}},{"language": "English"},{"avg_vote": {"$gt": int(minRating)}}, 
            {"year": {"$gt": int(minYear), "$lt":int(maxYear)}}]},{"_id":False})
    if mydoc.count() == 0:
        return None   
    numDoc = mydoc.count()
    #randomize index because mongodb has ordering
    randIndex = randrange(1,numDoc)
    index = 0
    for x in mydoc:
        index +=1
        if index == randIndex:
            if x in recMovieList:
                continue
            return x['original_title']

# generate a list of movies to watch
def generateMovList(minRating, minYear, maxYear):
    it = 0
    while it < 1000 and len(movieList) < 5:
        recMovie = pickMovie(movieList,minRating,minYear,maxYear)
        if recMovie not in movieList and recMovie is not None:
            movieList.append(recMovie)
        else:
            it+=1
    if it == 1000:
        print("you're group is unable to be satisfied, you might have to pick a different activity tonight")
    print(movieList)
    return movieList

    

insert("Biography", 1, 4, 5, 2)
insert("Crime", 5, 4, 4, 3)
insert("Drama", 5, 3, 4, 3)
insert("History", 1, 4, 5, 1)
insert("Adventure", 4, 3, 2, 4)
insert("Fantasy", 4, 3, 1, 1)
insert("War", 5, 3, 4, 2)
insert("Mystery", 4, 5, 3, 3)
insert("Horror", 5, 2, 1, 3)
insert("Western", 3, 2, 4, 2)
insert("Comedy", 3, 1, 4, 3)
insert("Family", 3, 1, 4, 3)
insert("Action", 5, 2, 2, 4)
insert("Sci-fi", 4, 5, 1, 5)
insert("Thriller", 5, 4, 3, 3)
insert("Sport", 3, 1, 5, 3)
insert("Animation", 3, 3, 1, 4)
insert("Musical", 3, 1, 3, 3)
insert("Film-Noir", 4, 4, 4, 2)
insert("Romance", 2, 1, 4, 3)
#diffDict = kClosest(1,4,5,3)
diffDict = kClosest(5,4,2,4)
setProbOfEachGenre()
generateMovList("1","1970","2000")

