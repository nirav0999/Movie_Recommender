
"""
Author-Nirav :D  
This is a bs4 Simulation to scrape IMDB
Through this ,we can access each individual author page 
"""
#from selenium import webdriver 
from bs4 import BeautifulSoup
# Install selenium by ------> python3 -m pip install --user selenium
#from bs4 import beautifulsoup4
import time
import re
import requests
from urllib.request import urlopen
import pymongo
from pymongo import MongoClient
import base64
import codecs

genres=["action","adventure","animation","biography","comedy","crime","drama","horror","musical","mystery","sci_fi","sport","thriller","western"]#List of Genres Picked by me

def seach_genres(str1):
	for i in allgenres:
		#print(i)
		if str(i)==str1:
			return True
	return False

def convert_img_to_bin(path):
	"""
	Input-pathto image file
	Default Format-.jpg
	//Recommended
	Returns an image file to a binary String
	"""
	with open(path, "rb") as imageFile:
		st1 = base64.b64encode(imageFile.read())
		#print (st1)
		return st1
def convert_bin_to_img(binstr,path):
	"""
	Input-binary_string,path
	Default Format-.jpg
	//Recommended
	Makes a image file at the specified path
	"""
	fh = open(path,"wb")
	fh.write(codecs.decode(binstr,'base64'))
	fh.close()

def insert_in_database(id1,name,genre,dor,summary,IMDBrating,nfvoters,imgbinary):
	"""
	Inserts a record into the the database
	"""
	rec= { 
		"_id":id1,
		"name":name, 
		"genre":genre,
		"dor":dor, 
		"summary":summary,
		"IMDBrating":IMDBrating,
		"nfvoters":nfvoters,
		"imgbin":imgbinary
		}
	collection.insert_one(rec)


def find_poster(htmldata,name):
	"""
	Finds the main image of the movie poster within the webpage and saves it at the specified path
	"""
	links = htmldata.find("div",class_="poster").find_all('img', src=True)
	for link in links:
		timestamp = time.asctime() 
		print(link)
		txt = open("Posters/"+name+".jpg", "wb")
		link = link["src"].split("src=")[-1]
		download_img = urlopen(link)
		txt.write(download_img.read())
		txt.close()
	return_path="Posters/"+name+".jpg"
	return return_path
	

def find_name(htmldata):
	"""
	Returns the name of the movie 
	"""
	for name in htmldata.findAll('h1'):
		x=name.contents[0]
		x1=x.replace("\xa0","")
		print(x1)
		return x1
def correct_genrelist(x):
	"""
	Parsing the genre ,Removing the abnormalities and adding in List
	"""
	genre_list=[]
	for k in x:
		k1=k.replace("-","_")
		k2=k1.replace(" ","")
		k3=k2.replace("\n","")
		k4=k3.replace('\xa0',"")
		k5=k4.lower()
		u=k5.split(":")
		if len(u)>1:
			#print(u[1])
			genre_list.append(str(u[1]))
		else:
			#print(u[0])
			genre_list.append(str(u[0]))
	return genre_list

def find_genres(htmldata):
	"""
	Returns the genre of the movies scraped
	"""
	g=htmldata.findAll('div',class_="see-more inline canwrap")
	x=g[1].text.split("|")
	g1=""
	genres_list=[]
	genres_list=correct_genrelist(x)
	if len(genres_list)>=2:
		for i in range(len(genres_list)):
			curr_element=str(genres_list[i])
			if curr_element in genres:
				#print("VALID GENRE->Adding to List")
				g1=g1+curr_element+" "
	
	print(g1)
	return g1

def find_rd(htmldata):
	"""
	Returns the Release Date of the movie 
	"""
	for date in htmldata.findAll('div',class_="subtext"):
		date1=date.findAll('a')
		len1=len(date1)
		release_date=date1[len1-1].text
		print(release_date)
		release_date=release_date.replace("\n","")
		return release_date

def find_summary(htmldata):
	"""
	Returns the Summary of the movie 
	"""
	y=htmldata.find('div',class_="summary_text")
	summary=y.contents
	summary1=summary[0].replace('\n',"")
	print(summary1)
	return summary1

def findIMdbrating(htmldata):
	"""
	Returns the IMDBRating and the No of Voters who have voted on it
	"""
	for d1 in htmldata.findAll('div',class_='ratingValue'):
		s=d1.find('strong')['title']
		x=s.split(" ")
		rating=x[0]
		nof=x[3]
		y=[x[0],x[3]]
		print("IMDB Rating=",x[0])
		print("Number of Voters=",x[3])
		return y
		#print(d1.find('strong').get_attribute('title'))



#MAIN CODE
client=""
try: 
	client=MongoClient() 
	print("Connected successfully!!!") 
except:   
	print("Could not connect to MongoDB") 

dbname='movie_collection'
db={}
db=client[dbname]
collection_name='movie'
collection={}
collection=db[collection_name]
#ng-src="data:image/jpeg;base64 >
#Visit imdb page to select your genres
movie_names=[]
#genre_counts=[]
#Base Link-https://www.imdb.com/search/title?genres=action&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=18DR95PBE7NRWQQ56RZZ&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_17
movie_count=0
for j in range(len(genres)):
	if j>=0:
		print("============================================Starting a new Genre========================================"+str(j))
		current_link="https://www.imdb.com/search/title?genres="+genres[j]+"&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=18DR95PBE7NRWQQ56RZZ&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_17"
		page=urlopen(current_link)
		soup=BeautifulSoup(page,"html.parser")
		movie_page_links=[]
		for search1 in soup.findAll('h3',class_="lister-item-header"):
			for search2 in search1.findAll('a'):
				movie_page_link=search2.get('href')
				movie_page_links.append(movie_page_link)
		print(len(movie_page_links))
		genre_count=0
		for movie_link in movie_page_links:
			if genre_count<=15:
				print("-------------------------------Scraping Movie Page---------------------------------------",genre_count)
				current_movie_link="https://www.imdb.com/"+movie_link
				page1=urlopen(current_movie_link)
				movie_html=BeautifulSoup(page1,"html.parser")
				name=find_name(movie_html)
				if name not in movie_names:
					movie_names.append(name)
					try:
						genre1=find_genres(movie_html)
						release_date=find_rd(movie_html)
						poster_path=find_poster(movie_html,name)
						summary=find_summary(movie_html)
						[IMDBrating,nfvoters]=findIMdbrating(movie_html)
						imgbin=convert_img_to_bin(poster_path)
						movie_id="m"+str(movie_count)
						print("		Adding to the Database------>")
						#insert_in_database(movie_id,name,genre1,release_date,summary,IMDBrating,nfvoters,imgbin)
						movie_count=movie_count+1
						genre_count=genre_count+1
						print("		Added to the Database")
					except:
						print("Skipping this one coz of some error")
				else:
					print(name," already included in Database ")
print("***********************Total_Number_of_Movies*************************",len(movie_names))
#print("Genre Counts-",genre_counts)	








