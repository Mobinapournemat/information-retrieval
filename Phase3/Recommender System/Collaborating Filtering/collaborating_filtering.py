import csv
from numpy import dot
from numpy.linalg import norm
import pandas as pd
import json

def collab_filtering(x, n):
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    for i in range(len(x)):
        if x[i] == '':
            x[i] = 0
            continue
        x[i] = float(x[i])
    sim = list()
    normx = norm(x)
    for i in range(1, 10001):
        profile = data[i]
        for j in range(len(profile)):
            if profile[j] == '':
                profile[j] = 0
                continue
            profile[j] = float(profile[j])
        normv = norm(profile)
        if normx == 0 or normv == 0:
            sim.append(0)
            continue
        cos_sim = dot(x, profile)/(normx*normv)
        sim.append(cos_sim)
    sim_s = pd.Series(sim)
    temp = sim_s.nlargest(n+1)
    indexes = temp.index.values.tolist()
    similar_profiles = list()
    similarities = list()
    for ind in range(1, len(indexes)):
        similar_profiles.append(data[indexes[ind]])
        similarities.append(sim[indexes[ind]])
    for i in range(len(x)):
        if x[i] != 0:
            continue
        summ = 0
        for j in range(len(similar_profiles)):
            summ += (similar_profiles[j][i] * similarities[j])
        avg = summ / sum(similarities)
        x[i] = avg
    summ = sum(x)
    x = [element * (1/summ) for element in x]
    print("Profile: ",x)

    f = open('content.json',)
    papers = json.load(f)
    n = len(papers)
    i = 0
    map_id = dict()
    for paper in papers:
        id = paper['id']
        map_id[i] = id
        i += 1
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    map_topics = dict()
    m = len(data[0])
    i = 0
    for topic in data[0]:
        map_topics[topic.lower()] = i
        i += 1

    v = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(len(papers)):
        paper = papers[i]
        rel_topics = paper['related_topics']
        for t in rel_topics:
            temp = map_topics.get(t.lower())
            if temp is None:
                continue
            v[i][temp] = 1

    similarities = [0 for _ in range(len(v))]
    normx = norm(x)
    for t in range(len(v)):
        vec = v[t]
        normv = norm(vec)
        if normx == 0 or normv == 0:
            similarities[t] = 0
            continue
        cos_sim = dot(x, vec)/(normx*normv)
        similarities[t] = cos_sim
    sim = pd.Series(similarities)
    temp = sim.nlargest(10)
    indexes = temp.index.values.tolist()
    for i in indexes:
        print("Paper id:",map_id[i]," => Similarity:", similarities[i])
        

# x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2094988621693399, 0.17113668350763622, 0.19553929265317616, 0, 0, 0, 0.2512692277040901, 0, 0.09000994237697385, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.08254599158878372]
# collab_filtering(x,20)