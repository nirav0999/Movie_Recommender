from flask import Flask, flash, redirect, render_template, request, session, abort,jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import importlib
import algos
#importlib.import_module('algos')

app = Flask(__name__,static_url_path='/static')

client = MongoClient('mongodb+srv://admin:pd1911@cluster0-gjqsc.mongodb.net/test?retryWrites=true')
db = client['movie_db']
global collection
collection = db['movies']
all_list=[]
machineList=[]
@app.route('/')
def home():
    mov = collection.find_one()
    return render_template('welcome.html', data=mov)  



@app.route('/get_data')
def get_data():
	#print(dumps(list(collection.find())))
	return dumps(list(collection.find()))


@app.route('/get_data1')
def get_data1():
	#return render_template('result.html')
	print("GETTING HERE")
	return dumps(machineList)


@app.route('/iget_back_data', methods=['POST', 'GET'])
def iget_back_data1():
	mids=[]
	if request.method == 'POST':
		json_str=request.get_json()
		#print("Client is asking for Item-Based Recommendation",json_str)
		mids=algos.Item_Rec_Handler(json_str)
		#print("Received",mids)
	machineList.clear()
	for mid in mids:
		ml=collection.find({"_id":mid})
		for ai in ml:
			#print("++++++++++++++++++++++++++++++++++++++++++++")
			#print(ai)
			item={
				'_id':ai['_id'],
				'name':ai['name'],
				'genre':ai['genre'],
				'dor':ai['dor'],
				'IMDBrating':ai['IMDBrating'],
				'summary':ai['summary'],
				'nfvoters':ai['nfvoters']
			}
			machineList.append(item)
	print(machineList[0],machineList[1],machineList[2])
	return dumps(machineList)
	"""
	a=[]
	for mid in mids:
		print(mid)
		x=dumps(collection.find({"_id":mid}))
		a.append(x)
	print(dumps(a))
	#return get_data1(dumps(a))
	return dumps(a)
	"""

@app.route('/uget_back_data', methods=['POST', 'GET'])
def uget_back_data2():
	mids=[]
	if request.method == 'POST':
		json_str=request.get_json()
		#print("Client is asking for User-Based Recommendation",json_str)
		mids=algos.User_Rec_Handler(json_str)
		#print("Received",mids)
	machineList.clear()
	for mid in mids:
		ml=collection.find({"_id":mid})
		for ai in ml:
			#print("++++++++++++++++++++++++++++++++++++++++++++")
			#print(ai)
			item={
				'_id':ai['_id'],
				'name':ai['name'],
				'genre':ai['genre'],
				'dor':ai['dor'],
				'IMDBrating':ai['IMDBrating'],
				'summary':ai['summary']
			}
			machineList.append(item)
	print(machineList[0],machineList[1],machineList[2])
	return dumps(machineList)
	"""
	a=[]
	for mid in mids:
		print(mid)
		x=collection.find_one({"_id":mid})
		print(x)
		a.append(x)
	print(collection.find_one({"_id":mid}))
	return dumps(collection.find_one({"_id":mid}))
	"""

@app.route('/mget_back_data', methods=['POST', 'GET'])
def mget_back_data3():
	mids=[]
	if request.method == 'POST':
		json_str=request.get_json()
		#print("Client is asking for Matrix-Based Recommendation",json_str)
		mids=algos.Matrix_Rec_Handler(json_str)
		#print("Received",mids)
	machineList.clear()
	for mid in mids:
		ml=collection.find({"_id":mid})
		for ai in ml:
			#print("++++++++++++++++++++++++++++++++++++++++++++")
			#print(ai)
			item={
				'_id':ai['_id'],
				'name':ai['name'],
				'genre':ai['genre'],
				'dor':ai['dor'],
				'IMDBrating':ai['IMDBrating'],
				'summary':ai['summary'],
				'nfvoters':ai['nfvoters']
			}
			machineList.append(item)
	print(machineList[0],machineList[1],machineList[2])
	return dumps(machineList)
	"""
	a=[]
	for mid in mids:
		print(mid)
		x=dumps(collection.find({"_id":mid}))
		print(x)
		a.append(x)
	print(dumps(a))
	return dumps(collection.find({"_id":mid}))
	"""
@app.route('/result')
def home1():
    return render_template('result.html')
if __name__ == "__main__":
	app.run()