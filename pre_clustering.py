from sklearn.cluster import KMeans
from OM_PY_utilities import *

def group_onsets(onsets, num_clusters):
    # Reshape the onsets array to a 2D array
    X = [[onset] for onset in onsets]

    # Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, n_init='auto')
    kmeans.fit(X)

    # Retrieve the cluster labels assigned to each onset
    labels = kmeans.labels_

    # Group the onsets based on the cluster labels
    groups = {}
    for i, label in enumerate(labels):
        if label not in groups:
            groups[label] = []
        groups[label].append(onsets[i])

    return groups