import numpy as np

def kmean(data,initial_centroids, max_iter):
    centroids = initial_centroids
    for _ in range(max_iter):
        dist = np.sum(np.sqrt((data[np.newaxis, :] - centroids[:, np.newaxis]) ** 2), axis=-1)
        # dist = distance.cdist(data, centroids, 'cityblock')
        assignments = np.argmin(dist, axis=0)
        new_centroids = np.array(
            [np.median(data[assignments == cluster], axis=0) for cluster in range(256)])
        index = set(np.arange(256)) - set(np.unique(assignments))
        index = np.array(list(index)).T
        new_centroids[index] = centroids[index]
        if (new_centroids == centroids).all():
            break
        centroids = new_centroids
    # more round of kmeans to get the new dot cluster
    dist = np.sum(np.sqrt((data[np.newaxis, :] - centroids[:, np.newaxis]) ** 2), axis=-1)
    assignments = np.argmin(dist, axis=0)
    new_centroids = np.array(
        [np.median(data[assignments == cluster], axis=0) for cluster in range(256)])
    index = set(np.arange(256)) - set(np.unique(assignments))
    index = np.array(list(index)).T
    new_centroids[index] = centroids[index]
    codebook = centroids
    code = assignments
 
    return codebook, code
 
 
 
def pq(data, P, init_centroids, max_iter):
 
    data = np.split(data, P, axis=1)
 
    center = []
 
    code = []
 
    for i in range(P):
 
        center_record, code_record = kmean(data[i], init_centroids[i], max_iter)
 
        center.append(center_record)
 
        code.append(code_record)
 
    return np.array(center,dtype = np.float32 ), np.array(code,dtype = 'uint8').T

def get_distance(centroids, query, codebooks):
    # centroids in the form of '[12, 34, 21, 56]'
    centroids = np.fromstring(centroids[1:-1], dtype = np.uint8, sep = ",")
    P = centroids.shape[0]
    query_partitions = np.split(query, P, axis=0)
    dist = 0.0
    for i in range(P):
        centroid = codebooks[i][centroids[i]]
        dist += np.sum(np.absolute(query_partitions[i]-centroid), axis = -1)
    return dist    

def query(queries, codebooks, codes, T):
    answers = []
    
    # build inverted index using codes 
    # centroids (str representation of a list) -> list of data points
    inverted_index = {}
    for i in range(codes.shape[0]):
        centroid = np.array2string(codes[i],separator = ",")
        if centroid in inverted_index:
            inverted_index[centroid].append(i)
        else:
            inverted_index[centroid] = [i]
    #print(inverted_index)
    for i in range(queries.shape[0]):  
        query = queries[i]
        distances = []
        for centroids in inverted_index.keys():
            dist = get_distance(centroids, query, codebooks)
            distances.append((centroids, dist))
        # sort centroids based on distance 
        distances.sort(key=lambda x:x[1]) 
        #print(distances)
        closest = []
        for d in distances:
            centroid = d[0]
            for data_point in inverted_index[centroid]:
                closest.append(data_point)
            if len(closest) >= T:
                break
        answers.append(set(closest))

    return answers
