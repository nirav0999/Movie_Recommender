import numpy as np 
import pandas as pd
import sklearn
import scipy
from sklearn.metrics import pairwise_distances
from scipy.sparse.linalg import svds
from random import randint
from sklearn.metrics import mean_squared_error
import pymongo
from pymongo import MongoClient
"""
def get_mse(pred, actual):
	# Ignore nonzero terms.
	pred = pred[actual.nonzero()].flatten()
	actual = actual[actual.nonzero()].flatten()
	return mean_squared_error(pred, actual)

def pearson_correlation(train):
	item_correlation = 1 - pairwise_distances(train.T, metric='correlation')
	item_correlation[np.isnan(item_correlation)]=0
"""
"""
client=""
try: 
	client=MongoClient() 
	print("Connected successfully!!!") 
except:   
	print("Could not connect to MongoDB") 

dbname='user_collection'
db={}
db=client[dbname]
collection_name='user'
collection={}
collection=db[collection_name]
"""





def fetch_user(user_id):
	#Untested
	#Unused
	"""
	Returns a user from the MongoDB
	"""
	return ucollection.find_one({ "_id":user_id})
def fetch_user_ratings(user_id):
	#Untested
	"""
	Returns the user ratings as a list
	"""
	user=ucollection.find_one({ "_id":user_id})
	ratings_as_string=user['user_ratings']
	ratings_as_num=ratings_int(ratings_as_string)
	return ratings_as_num
	
def ratings_int(ratings_string):
	"""
	Inputs a Ratings _String
	Returns a Ratings Integer List 
	"""
	r=ratings_string.split(" ")
	ratings=[]
	for i in r:
		ratings.append(int(i))
	return ratings
def ratings_string(ratings_int):
	"""
	Inputs a ratings_int_list
	returns 
	"""
	ratings_string=ratings_int[0]
	for j in range(1,len(ratings_int)):
		ratings_string=ratings_as_string+" "+ratings_int[j]
	return ratings_string





#MAIN CODE
uclient=""
try: 
	uclient=MongoClient() 
	print("Connected successfully!!!") 
except:   
	print("Could not connect to MongoDB") 

dbname='movie_collection'
db={}
db=uclient[dbname]
mcollection_name="movie"
ucollection_name="user"
ucollection={}
mcollection={}
ucollection=db[ucollection_name]
mcollection=db[mcollection_name]


ratings=create_dummy_users()
R = ratings
user_ratings_mean = np.mean(R, axis = 1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)

U, sigma, Vt = svds(R_demeaned, k = 25)
sigma = np.diag(sigma)
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings)

print(preds_df.iloc[[2]])
