def aggResults(arrInputs):
    #thrill, brainpower, realism, futurism
    thrill = 0
    brainpower = 0
    realism = 0
    futurism = 0
    for results in arrInputs:
        thrill += results[0]
        brainpower += results[1]
        realism += results[2]
        futurism += results[3]
    thrill /= len(arrInputs)
    brainpower /= len(arrInputs)
    realism /= len(arrInputs)
    futurism /= len(arrInputs)
    return [thrill, brainpower, realism, futurism]

def voteAggregation(ratingInputs):
    return list(map(sum, zip(*ratingInputs)))
