import json
import csv
from numpy import dot
from numpy.linalg import norm
import pandas as pd

def content_based(x, v):
    for i in range(len(x)):
        if x[i] == '':
            x[i] = 0
            continue
        x[i] = float(x[i])
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


content_based(data[148], v)


