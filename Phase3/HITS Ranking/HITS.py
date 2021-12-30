import json
import pandas as pd

def get_authors_rank(path, number):
    f = open(path,)
    data = json.load(f)
    map_paper = dict()
    map_author = dict()
    map_author_rev = dict()
    i, j = 0, 0
    for paper in data:
        id = paper['id']
        map_paper[id] = j
        j += 1
        authors = paper['authors']
        for a in authors:
            if a == '':
                continue
            if map_author.get(a) is not None:
                continue
            map_author[a] = i
            map_author_rev[i] = a
            i += 1
    n = len(map_author)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    for paper in data:
        x = paper['authors']
        for ref in paper['references']:
            index = map_paper.get(ref)
            if index is None:
                continue
            y = data[index]['authors']
            for a in x:
                if a == '':
                    continue
                i = map_author[a]
                for b in y:
                    if b == '':
                        continue
                    j = map_author[b]
                    adj[i][j] = 1

    hub = [1 for _ in range(n)]
    authority = [1 for _ in range(n)]   
    for counter in range(5):
        for i in range(n):
            points_to = adj[i]
            summ = 0
            for j in range(n):
                if points_to[j] == 0:
                    continue
                summ += authority[j]
            hub[i] = summ
        for j in range(n):
            summ = 0
            for i in range(n):
                if adj[i][j] == 0:
                    continue
                summ += hub[i]
            authority[j] = summ
        sum_hub = sum(hub)
        hub = [element * (1/sum_hub) for element in hub]
        sum_authority = sum(authority)
        authority = [element * (1/sum_authority) for element in authority]

    authority_s = pd.Series(authority)
    temp = authority_s.nlargest(number)
    indexes = temp.index.values.tolist()
    for i in indexes:
        print(map_author_rev[i]," => ", authority[i])


#get_authors_rank('content.json', 25)