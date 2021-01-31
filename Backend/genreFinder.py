from pprint import pprint
genreGraph = {}
diffDict = {}
def insert(genre, thrill, brainpower, realism, futurism):
    genreGraph[genre] = [thrill,brainpower,realism,futurism]

def kClosest(thrill,brainpower,realism,futurism):
    for genre in genreGraph:
        genreThrill = genreGraph[genre][0]
        genreBP = genreGraph[genre][1]
        genreRealism = genreGraph[genre][2]
        genreFuturism = genreGraph[genre][3]
        diffDict[genre] = (thrill - genreThrill) ** 2 + (brainpower - genreBP) **2 + \
            (realism - genreRealism) **2 + (futurism - genreFuturism) **2
    
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
pprint(genreGraph)
kClosest(3,5,2,1)
sorted_x = sorted(diffDict.items(), key=lambda kv: kv[1])
pprint(sorted_x)

