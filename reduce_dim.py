import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA

import umap
import hdbscan

print("Loading embeddings...")

with open('embed.npy', 'rb') as f:
    embeddings = np.load(f,allow_pickle=True)

scaledvecs = StandardScaler().fit_transform(embeddings)

print("Reducing dimensions to cluster...")
reducer = umap.UMAP(n_components=10, n_neighbors=60, random_state=42, metric='cosine', min_dist=0.0)
emb_reduced = reducer.fit_transform(scaledvecs)

print("Clustering...")
clusterer = hdbscan.HDBSCAN(min_cluster_size=30, min_samples=10)
found_clusters = clusterer.fit_predict(emb_reduced)

print("Reducing dimensions to plot...")
reducer = umap.UMAP(n_neighbors=60, random_state=42, metric='cosine', min_dist=0.0)
emb_reduced = reducer.fit_transform(scaledvecs)

print("Loading original data...")
df = pd.read_csv("full_docs.csv")
df.fillna('',inplace=True)

df['cluster'] = found_clusters

print("Ploting heatmap...")
pubcount = df.groupby('pubname').title.count()
keeppubs = pubcount[pubcount > 30].index
sample = df[df.pubname.isin(keeppubs)]
ct = pd.crosstab(sample.cluster, sample.pubname, normalize="columns")

plt.figure()
sns.heatmap(ct)

print("Ploting barplot...")
plt.figure()
cluster_pct = df.groupby('cluster').count() / len(df.index)
ax= sns.barplot(cluster_pct.index, cluster_pct.title)
ax.set(xlabel='Cluster', ylabel='Percentage')

print("Ploting scatter...")
if emb_reduced.shape[1] > 2:
    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)

    ax.scatter(emb_reduced[:, 0], emb_reduced[:, 1], emb_reduced[:, 2], c=found_clusters,
           cmap=plt.cm.Set1, edgecolor=None, s=4, alpha=0.7)

    ax.set_title("First three PCA directions")
    ax.set_xlabel("1st eigenvector")
    ax.w_xaxis.set_ticklabels([])
    ax.set_ylabel("2nd eigenvector")
    ax.w_yaxis.set_ticklabels([])
    ax.set_zlabel("3rd eigenvector")
    ax.w_zaxis.set_ticklabels([])

else:
    plt.figure()
    sns.scatterplot(emb_reduced[:,0], emb_reduced[:,1], hue=found_clusters, size=4, alpha=0.8, legend="full", palette="deep")
    #plt.scatter(emb_reduced[:,0], emb_reduced[:,1], c=found_clusters,
    #        cmap=plt.cm.Set1, edgecolor=None, s=4, alpha=0.7)

plt.show()