import numpy as np
import random
from pprint import pprint
from heapq import nsmallest 
from random import randrange
genreGraph = {}
diffDict = {}
probDict = {}

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
def pickMovie(minRating, minYear, maxYear):
    numOfGenres = randrange(1,4)
    genreList = random.choices(list(probDict.keys()), weights=probDict.values(), k=numOfGenres)
    print(genreList)
    

    

insert("biography", 1, 4, 5, 2)
insert("crime", 5, 4, 4, 3)
insert("drama", 5, 3, 4, 3)
insert("history", 1, 4, 5, 1)
insert("adventure", 4, 3, 2, 4)
insert("fantasy", 4, 3, 1, 1)
insert("war", 5, 3, 4, 2)
insert("mystery", 4, 5, 3, 3)
insert("horror", 5, 2, 1, 3)
insert("western", 3, 2, 4, 2)
insert("comedy", 3, 1, 4, 3)
insert("family", 3, 1, 4, 3)
insert("action", 5, 2, 2, 4)
insert("sci-fi", 4, 5, 1, 5)
insert("thriller", 5, 4, 3, 3)
insert("sport", 3, 1, 5, 3)
insert("animation", 3, 3, 1, 4)
insert("musical", 3, 1, 3, 3)
insert("film-noir", 4, 4, 4, 2)
insert("romance", 2, 1, 4, 3)
diffDict = kClosest(1,4,5,3)
setProbOfEachGenre()
pickMovie(1,1,1)


