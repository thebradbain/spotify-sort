import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import cluster, decomposition

songs = pd.read_csv("data/spotify.dat")
labels = songs.values[:,1]
X = songs.values[:,2:]

kmeans = cluster.AffinityPropagation(preference=-200)
kmeans.fit(X)

predictions = {}
for p,n in zip(kmeans.predict(X),labels):
	if not predictions.get(p):
		predictions[p] = []

	predictions[p] += [n]

for p in predictions:
	print "Category",p
	print "-----"
	for n in predictions[p]:
		print n
	
	print ""