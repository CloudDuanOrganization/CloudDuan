__author__ = 'wangzhuo'

from math import sqrt
from collections import defaultdict

# 采用向量距离的方式判断两个人的相似度
def sim_distance(prefs,person1,person2):
    si = []
    for item in prefs[person1]:
        if item in prefs[person2]:
            si.append((prefs[person1][item] - prefs[person2][item])**2)
    if len(si) == 0:
        return 0
    # print (si)
    return 1 / (1 + sqrt(sum(si)))

# 采用pearson相似度判断两个人的相似度
def sim_pearson(prefs,personx,persony):
    n = 0
    sumx = sumy = sumSqx = sumSqy = sumP =0
    for item in prefs[personx]:
        if item in prefs[persony]:
            n += 1
            sumx += prefs[personx][item]
            sumy += prefs[persony][item]
            sumSqx += prefs[personx][item]**2
            sumSqy += prefs[persony][item]**2
            sumP += prefs[personx][item]*prefs[persony][item]
    if n == 0:
        return 0
    lxx = sumSqx - sumx**2 / n
    lxy = sumP - sumx*sumy / n
    lyy = sumSqy - sumy**2 / n
    if lxx*lyy == 0:
        return 0
    return lxy / sqrt(lxx * lyy)


def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(other,similarity(prefs,person,other))
            for other in prefs if other != person]
    scores.sort(key= lambda x: x[1],reverse=True)
    return scores[0:n]


def getRecommendations(prefs,person,similarity=sim_pearson):
    print(prefs)
    totals = defaultdict(lambda : 0.00000000001)
    simSums = defaultdict(lambda : 0.00000000001)
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs,person,other)
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person]:
               totals[item] += prefs[other][item] * sim
               simSums[item] += sim
    rankings = [(item,totals[item]/simSums[item]) for item in totals]
    rankings.sort(key=lambda x:x[1],reverse=True)
    return rankings


def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs,n=10):
    result = {}
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c += 1
        if c % 100 == 0:print ('%d / %d' % (c,len(itemPrefs)))
        scores = topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item] = scores
        # print('###########')
        # print(item)
        # print(scores)
        # print('###########')
    return result

# 使用用户之间的相似度作为加权平均系数，然后给想要得到推荐的用户没看过
# 的但其他用户已浏览过的段子进行打分，分高的段子则是适合该用户的，将会率先推荐给用户
def getRecommendedItems(prefs,itemMatch,user):
    userRatings = prefs[user]
    totalSim = defaultdict(lambda :0.00000000001)
    scores = defaultdict(lambda :0.00000000001)
    for (item,rating) in userRatings.items():
        for (item2,similarity) in itemMatch[item]:
            if item2 not in userRatings:
                scores[item2] += similarity * rating
                totalSim[item2] += similarity
    rankings = [(item,scores[item]/totalSim[item]) for item in scores]
    rankings.sort(key=lambda x : x[1],reverse = True)
    return rankings


def loadMovieLens():
    movies = {}
    prefs = defaultdict(dict)
    for line in open('u1.item'):
        (id,title) = line.split('|')[0:2]
        movies[id] = title
    for line in open('u.data'):
        (user,movieid,rating,ts) = line.split('\t')
        prefs[user][movies[movieid]] = float(rating)
    return prefs
