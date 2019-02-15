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
#print(collection.find({}))
for i in range(221):
	movie_id="m"+str(i)
	for doc in collection.find({"_id":movie_id}):
		print(doc["name"])
		name="Thumbnails/"+movie_id+".jpg"
		convert_bin_to_img(doc["imgbin"],name)
