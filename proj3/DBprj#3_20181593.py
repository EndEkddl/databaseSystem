#-*- coding: utf-8 -*-
import datetime
import time
import sys
import MeCab
import operator
from pymongo import MongoClient
from bson import ObjectId
from itertools import combinations
from math import log
import math
import re


def printMenu():
    print "1. WordCount"
    print "2. TF-IDF"
    print "3. Similarity"
    print "4. MorpAnalysis"
    print "5. CopyData"

#In this project, we assume a word seperated by a space is a morpheme.

def MorphAnalysis(docs, col_tfidf):
	print("\nMorphAnalysis")
	
	# Step(1) Read stopword list from file named stopword_list.txt
	stop_word = {}
	f = open("stopword_list.txt", "r")
	while True:
		line = f.readline()
		if not line: break
		stop_word[line.strip('\n')] = line.strip('\n')
	f.close()

	# Step(2) Analysis Morpheme in given text and delete stopword
	for doc in docs:
		content = doc['text']
		# Delete non-ahphabetical characters
		content = re.sub('[^a-zA-Z]', ' ', content)
		# Change all captical letter to small letter
		content = content.lower().split()

		# Delete stopword in a given text dataset
		MorpList = []

		for arg in content:
			if not arg in stop_word:
				MorpList.append(arg)
	# Step(3) Store processed morpheme data into MongoDB
		col_tfidf.update({'_id':doc['_id']}, {'$set': {'morph': MorpList}}, True)
	
	id = str(raw_input("Enter the object id of tweet : "))
	print("\n==List of morphemes in the tweet corresponding to the id you entered==")	
	for docs in col_tfidf.find():
		if(str(docs['_id'])==id):
			for w in docs['morph']:
				print(w.encode('utf-8'))

	
def WordCount(docs, col_tfidf):
	print("\nWordCount")
#	arr = []
#	n = docs.count()

	for doc in docs:
		arr = []
		arr.append([])
		morph = doc['morph']
		n = len(morph)
		for i in range(n):
			term = morph[i]
			tf = morph.count(term)
			arr[-1].append(tf)
			col_tfidf.update({'_id':doc['_id']}, {'$set': {'wordcount': arr}}, True)


	id = str(raw_input("Enter the object id of tweet : "))
	print("\n==Number of words in the tweet corresponding to the id you entered==")	

	for docs in col_tfidf.find():
		if(str(docs['_id'])==id):
			n = len(docs['wordcount'])
			for i in range(n):
				print(docs['wordcount'][i] )
			#print(docs['wordcount'])
	
#	for docs in col_tfidf.find():
#		if(str(docs['_id'])==id):
#			print(len(docs['morph']))

def idf(docs, word):
	df = 0
	for doc in docs:
		if(doc['morph'].count(word) > 0): 
			df += 1
	
	print("df : ", df)	
	if(df==0):
		return 0
	else : 
		return math.log(1101/df)

def TfIdf(docs, col_tfidf):
	print("\nTF-IDF")
	id = str(raw_input("Enter the object id of tweet : "))
	for doc in docs:
		if(str(doc['_id'])==id):
			arr = []
			cnt = len(doc['morph'])
			for i in range(cnt):
				word = doc['morph'][i]
				print(word)
				TF = doc['wordcount'][0][i]
				TF /= cnt
				IDF = idf(docs, word)
				print("tf" , TF, "IDf" , IDF)
				arr.append(TF*IDF)
	
	print(arr)	
			
		

def Similarity(docs, col_tfidf):
	print("\nSimiliarity")
	#TO-DO in project

def copyData(docs, col_tfidf):
	col_tfidf.drop()
	for doc in docs:
		contentDic = {}
		for key in doc.keys():
			if key != "_id":
				contentDic[key] = doc[key]
		col_tfidf.insert(contentDic)
	
#Access MongoDB
conn = MongoClient('localhost')

#fill it with your DB name - db+studentID ex) db20120121
db = conn['db20181593']

#fill it with your MongoDB( db + Student ID) ID and Password(default : 1234)
db.authenticate('db20181593', '1234')

col = db['tweet']
col_tfidf = db['tweet_tfidf']

if __name__ == "__main__":
	printMenu()
	selector = input()
	
	if selector == 1:
		docs = col_tfidf.find()
        	WordCount(docs, col_tfidf)

	elif selector == 2:
        	docs = col_tfidf.find()	
		TfIdf(docs, col_tfidf)
    
	elif selector == 3:
		Similarity(docs, col_tfidf)

	elif selector == 4:
		docs = col_tfidf.find()
		MorphAnalysis(docs, col_tfidf)
	
	elif selector == 5:
		docs = col.find()
		copyData(docs,col_tfidf)
