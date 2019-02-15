import numpy as np 
import pandas as pd
#import sklearn
#import scipy
#from sklearn.metrics import pairwise_distances
#from scipy.sparse.linalg import svds
from random import randint
#from sklearn.metrics import mean_squared_error
import pymongo
from pymongo import MongoClient
import math
from pandas.testing import assert_frame_equal
from scipy.sparse.linalg import svds
import json

#--------------------------USER_Functions-------------------------------------------------------
"""
TC
Input-nfusers,nfmovies,numberof movies to be rated by the dummy user
---------
Function-Creates Dummy Users for the Ratings_Matrix and stores the Matrix 
in a CSV by the name Ratings_Matrix.All the users rate any movies randomly 
---------
Returns-nfusers x nfmovies matrix of randomly rated movies
"""
def create_dummy_users(nfusers,nfmovies,nfmoviesrated):
	ratings=np.zeros((nfusers,nfmovies))
	for i in range(nfusers):
		uid="u"+str(i)
		rate=[]
		for k in range(nfmovies):
			rate.append(0.00000)
		nfmoviesratedbyuser=nfmoviesrated
		for j in range(nfmoviesratedbyuser):
			movie_id=randint(0,220)
			if ratings[i][movie_id]==0:
				movie_rating=randint(1,5)
				ratings[i][movie_id]=movie_rating
				rate[movie_id]=movie_rating
			else:
				j=j-1
	#print(ratings)
	return ratings

"""
UC
Input-User_Ratings in a integer array of nfmovies
---------
Function-Adds the the new user and her ratings in the CSV Ratings_Matrix 
---------
Returns the user_id of the newly_formed user
"""
def add_user(user_ratings):
	ratings_matrix=pd.read_csv("RatingsMatrix",sep=' ')
	ratings_matrix=ratings_matrix.loc[:, ~ratings_matrix.columns.str.contains('^Unnamed')]
	nfusers,nfmovies=ratings_matrix.shape
	user_ratings=pd.DataFrame(user_ratings)
	ratings_matrix.loc[nfusers]=user_ratings
	ratings_matrix.to_csv("RatingsMatrix", sep=' ')
	user_id="u"+str(nfusers)
	return user_id


"""
TC
Input-Ratings_Matrix,nfusers,nfmovies,nfmoviesratedbyuser=5
---------
Calculates the Average of each user's ratings and stores it in the Dataframe
---------
Returns the modified_ratings_matrix with the average_ratings of each user 
"""
def add_calc_avg_matrix(ratings_matrix,nfusers,nfmovies,nfmoviesratedbyuser=10):
	ratings_matrix['average_rating']=0.00000
	for user in range(nfusers):
		userrating_sum=0.00000
		for movie in range(nfmovies):
			userrating_sum=userrating_sum+ratings_matrix.iloc[user,movie]
		userratingavg=float(float(userrating_sum)/nfmoviesratedbyuser)
		ratings_matrix.at[user,'average_rating']=float(userratingavg)
	return ratings_matrix

"""
TC
Input-user1,Modified_Ratings_matrix with average_ratings column added to it,nfusers,nfmovies
---------
Function-Calculates the Pearson Similarity of each user with the user1
---------
Returns the modified Ratings_Matrix with both the 
"""
def pearson_sim(user1,ratings_matrix,nfusers,nfmovies):
	
	nfusers,nfmovies=ratings_matrix.shape
	ratings_matrix['similarity']=0.00000
	#print(ratings_matrix)
	for user in range(nfusers):
		par1=0.00000
		par2=0.00000
		par3=0.00000
		nf_common_items=0
		for movie in range(nfmovies):
			nf_common_items=nf_common_items+1
			user_movie_rating=ratings_matrix.iloc[user,movie]
			user1_movie_rating=ratings_matrix.iloc[user1,movie]
			if user_movie_rating!=0 and user1_movie_rating!=0:
				x=user_movie_rating-ratings_matrix.iloc[user,221]
				y=user1_movie_rating-ratings_matrix.iloc[user1,221]
				par1=par1+x*y
				par2=par2+(x**2)
				par3=par3+(y**2)
		par2=round(math.sqrt(float(par2)),5)
		par3=round(math.sqrt(float(par3)),5)
		if par2!=0 and par3!=0:
			pearson=round(float(par1)/float(par2*par3),5)
			ratings_matrix.at[user,'similarity']=pearson
		else:
			ratings_matrix.at[user,'similarity']=0
	#print("After Calculating Pearson Similarities")
	#print(ratings_matrix)
	return ratings_matrix


"""
TC
Input-user1,Modified_Ratings_matrix with average_ratings column added to it,nfusers,nfmovies
---------
Function-Calculates the Pearson Similarity of each user with the user1
---------
Returns the modified Ratings_Matrix with both the 
"""
def Matrix_Decomposition(ratings):
	preds_df=[]
	R=ratings.as_matrix()
	user_ratings_mean=np.mean(R, axis = 1)
	R_demeaned=R-user_ratings_mean.reshape(-1, 1)
	a,sigma,b=svds(R_demeaned, k = 25)
	sigma=np.diag(sigma)
	all_user_predicted_ratings=np.dot(np.dot(a, sigma),b)+user_ratings_mean.reshape(-1, 1)
	predictions=pd.DataFrame(all_user_predicted_ratings)
	#print(predictions)
	return predictions

"""
Input-Original Rating's Matrix,nfusers,nfmovies
-----------------
Calculates the Adjusted_Cosine Similarity of each item with another 
by creating a nfmoviesxnfmovies matrix
------------------	
Returns-nfmoviesxnfmovies item's matrix with (i,j) cell denoting 
the adjusted cosine of movie i with movie j 
"""




def adjusted_cosine(ratings_matrix,nfusers,nfmovies):
	item_ratings_matrix=np.zeros((nfmovies,nfmovies))
	#print(ratings_matrix)
	for movie1 in range(nfmovies):
		for movie2 in range(nfmovies):
			par1=0.00000
			par2=0.00000
			par3=0.00000
			#print(ratings_matrix.loc['0','0'])
			for user in range(nfusers):
				if ratings_matrix.loc[user,str(movie1)]!=0.0000 and ratings_matrix.loc[user,str(movie2)]!=0.0000:
					x=ratings_matrix.loc[user,str(movie1)]-ratings_matrix.loc[user,'average_rating']
					y=ratings_matrix.loc[user,str(movie2)]-ratings_matrix.loc[user,'average_rating']
					par1=par1+(x*y)
					par2=par2+(x**2)
					par3=par3+(y**2)

			par2=float(math.sqrt(par2))
			par3=float(math.sqrt(par3))
			if par2!=0.0000 and par3!=0.0000:
				adjusted_cosine_sim=float(par1)/(par2*par3)
				item_ratings_matrix[movie1][movie2]=adjusted_cosine_sim
			else:
				item_ratings_matrix[movie1][movie2]=0.00000
	item_ratings_matrix=pd.DataFrame(item_ratings_matrix)
	#print("Items Rating Matrix=")
	#print(item_ratings_matrix)
	return item_ratings_matrix
	

#----------------------------------RECOMMENDER FUNCTIONS---------------------------------------------

"""
Input-User1,item_ratings_matrix,ratings_matrix,nfusers,nfmovies
Calculates the item_item_recommendation
Returns
"""
def item_recommend_movies(user1,item_ratings_matrix,ratings_matrix,nfusers,nfmovies):
	
	user1_rated_movies=[]
	for i in range(nfmovies):
		if ratings_matrix.loc[user1,str(i)]!=0:
				user1_rated_movies.append(i)
	recommended_items=[]
	for user1_rated_movie in user1_rated_movies:
		item_ratings_matrix=item_ratings_matrix.drop(user1_rated_movie)
		#print(item_ratings_matrix)
		recommended_items1=item_ratings_matrix.sort_values(by=[user1_rated_movie],ascending=False).head(10)
		for i in range(10):
			r1=recommended_items1.iloc[[i]].index.tolist()
			if int(r1[0]) not in recommended_items:
				recommended_items.append(int(r1[0]))
				break
	
	return recommended_items
"""
Arguments-user1,modified_ratings_matrix(with average and pearson_similarity in new columns),nfusers,nfmovies
We will Calculate which movies to show to our user by applying the extension of the algorithm
	
"""

def user_recommend_movies(user1,ratings_matrix,nfusers,nfmovies):
	user1_data=ratings_matrix.iloc[[user1]]
	ratings_matrix=ratings_matrix.round(10)
	ratings_matrix=ratings_matrix.drop(user1)
	sorted_matrix=ratings_matrix.sort_values(by=['similarity'],ascending=False).head(10)
	rec=[]
	for k in range(221):
		rec.append([0,0])
	for movie in range(221):
		par1=0.00000
		par2=0.00000
		for user in range(10):
			current_user_data=sorted_matrix.iloc[[user]]
			if current_user_data.iloc[0,222]>0.0:
				if user1_data.iloc[0,movie]==0 and current_user_data.iloc[0,movie]!=0:
					par1=par1+(current_user_data.iloc[0,222]*float((current_user_data.iloc[0,movie])-current_user_data.iloc[0,222]))
					par2=par2+abs(current_user_data.iloc[0,222])
		rec[movie][0]=movie
		if par1!=0 and par2!=0:
			par3=float(par1)/float(par2)
			rec[movie][1]=par3
		else:
			rec[movie][1]=0
	reccom=pd.DataFrame(rec)
	recommended_top_movies=reccom.sort_values(by=[1],ascending=False).head(10)
	print(recommended_top_movies.index.tolist())
	return recommended_top_movies.index.tolist()
def Matrix_recommend(user1,ratings_matrix,predictions,nfusers,nfmovies):
	rated_index=[]
	#print(ratings_matrix.iloc[user1])
	for movie in range(nfmovies):
		if ratings_matrix.iloc[user1,movie]!=0:
			rated_index.append(movie)
	#print("Movies Rated By User")
	#print(rated_index)
	#print(predictions.iloc[user1])
	predictions=predictions.drop(rated_index,axis=1)
	sorted_user_predictions = predictions.iloc[user1].sort_values(ascending=False)
	#print("Movies Recommended by Us:")
	recommended_movies=sorted_user_predictions.head(10).index.tolist()
	#print(recommended_movies)
	return recommended_movies


"""
Arguments-Dictionary in which key=movie_index(int) and value=rating of the movie
---------
Function-Adds and Creates  
---------
Returns User_ID and Ratings_Matrix with the new user ID
"""

def create_and_add_user(user_ratings):
	print("Importing Rating's Matrix...........")
	ratings_matrix=pd.read_csv("RatingsMatrix",sep=' ')
	ratings_matrix=ratings_matrix.loc[:, ~ratings_matrix.columns.str.contains('^Unnamed')]
	print("Imported Rating's Matrix :-)")
	nfusers,nfmovies=ratings_matrix.shape
	print("Current Number of Users=",nfusers)
	print("Current Number of Movies=",nfmovies)
	user_ratings1=[]
	for i in range(nfmovies):
		user_ratings1.append(0)
	for key,value in user_ratings.items():
		user_ratings1[int(key)]=value
	print("Creating and Adding User.........")
	user_ratings=pd.DataFrame(user_ratings1)
	user_id="u"+str(nfusers)
	ratings_matrix.loc[nfusers]=user_ratings1
	print("Created and Added user no.",user_id)
	print("Saving matrix back.........")
	ratings_matrix.to_csv("RatingsMatrix", sep=' ')
	print("Matrix Saved back Successfully :-)")
	#print("Ratings-Matrix")
	#print(ratings_matrix)
	return user_id,ratings_matrix

def User_Rec_Handler(jsonstr):
	#jsonsrt=requests.get()
	user_ratings={}
	for jsonstr1 in jsonstr["data"]:
		jsonstr1=json.loads(jsonstr1)
		m_id=jsonstr1["id"]
		movie_rating=int(jsonstr1["value"])
		movie_id=int(m_id.split("m")[1])
		user_ratings[movie_id]=movie_rating
	#print(type(user_ratings))
	user_id,ratings_matrix=create_and_add_user(user_ratings)
	user_index=int(user_id.split("u")[1])
	nfusers,nfmovies=ratings_matrix.shape
	ratings_matrix=add_calc_avg_matrix(ratings_matrix,nfusers,nfmovies,10)
	ratings_matrix=pearson_sim(user_index,ratings_matrix,nfusers,nfmovies)
	recommended_movies=user_recommend_movies(user_index,ratings_matrix,nfusers,nfmovies)
	#print(recommended_movies)
	return gen_Mongo_DB_id_string(recommended_movies)

def Item_Rec_Handler(jsonstr):
	user_ratings={}
	for jsonstr1 in jsonstr["data"]:
		jsonstr1=json.loads(jsonstr1)
		m_id=jsonstr1["id"]
		movie_rating=int(jsonstr1["value"])
		movie_id=int(m_id.split("m")[1])
		user_ratings[movie_id]=movie_rating
	#print(type(user_ratings))
	user_id,ratings_matrix=create_and_add_user(user_ratings)
	user_index=int(user_id.split("u")[1])
	nfusers,nfmovies=ratings_matrix.shape
	ratings_matrix=add_calc_avg_matrix(ratings_matrix,nfusers,nfmovies,10)
	item_ratings_matrix=adjusted_cosine(ratings_matrix,nfusers,nfmovies)
	recommended_movies=item_recommend_movies(user_index,item_ratings_matrix,ratings_matrix,nfusers,nfmovies)
	#print(recommended_movies)
	return gen_Mongo_DB_id_string(recommended_movies)

def Matrix_Rec_Handler(jsonstr):
	user_ratings={}
	for jsonstr1 in jsonstr["data"]:
		jsonstr1=json.loads(jsonstr1)
		m_id=jsonstr1["id"]
		movie_rating=int(jsonstr1["value"])
		movie_id=int(m_id.split("m")[1])
		user_ratings[movie_id]=movie_rating
	#print(type(user_ratings))
	user_id,ratings_matrix=create_and_add_user(user_ratings)
	user_index=int(user_id.split("u")[1])
	nfusers,nfmovies=ratings_matrix.shape
	predictions=Matrix_Decomposition(ratings_matrix)
	recommended_movies=Matrix_recommend(user_index,ratings_matrix,predictions,nfusers,nfmovies)
	#print(recommended_movies)
	return gen_Mongo_DB_id_string(recommended_movies)
def gen_Mongo_DB_id_string(recommended_movies):
	mid_arr=[]
	for i in recommended_movies:
		mid="m"+str(i)
		mid_arr.append(mid)
	print("Movies to be Recommended:")
	print(mid_arr)
	return mid_arr
#{"_id" : { "$in" : [  
#"55880c251df42d0466919268","55bf528e69b70ae79be35006" ]}}	



