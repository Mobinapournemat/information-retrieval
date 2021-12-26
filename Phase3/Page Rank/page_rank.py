import json
import numpy as np
  
def get_page_rank(read_path, alpha, write_path):
    f = open(read_path,)
    data = json.load(f)
    n = len(data)
    i = 0
    map_id = dict()
    map_id_rev = dict()
    for paper in data:
        id = paper['id']
        map_id[id] = i
        map_id_rev[i] = id
        i += 1
    p = [[0 for i in range(n)] for j in range(n)]
    for paper in data:
        for ref in paper['references']:
            i = map_id[paper['id']]
            j = map_id.get(ref)
            if j is None:
                continue
            p[i][j] = 1
    for i in range(n):
        summ = sum(p[i])
        if summ != 0:
            p[i] = [element * (1/summ) for element in p[i]]
        else:
            p[i] = [(1/n) for element in p[i]]
        p[i] = [element*(1-alpha)+(alpha/n) for element in p[i]]
    x = [1/n] * n
    x = np.matrix(x)
    p = np.matrix(p)
    a = x
    for i in range(50):
        a *= p
    a = a.tolist()[0]
    page_ranks = dict()
    for i in range(n):
        id = map_id_rev[i]
        rank = a[i]
        page_ranks[id] = str(rank)
    
    with open(write_path, 'w') as fp:
        json.dump(page_ranks, fp, indent=4)
    print("Ranking results saved!")


#get_page_rank('content.json', 0.1, 'CrawledPapers.json')
        


