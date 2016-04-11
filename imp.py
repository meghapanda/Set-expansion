import json
import numpy as np
from skimage.filters import threshold_otsu
import math
import timeit
from scipy.spatial.distance import cosine

file = open("word_list_100.json")
json1_str = file.read()
word_list=json.loads(json1_str)
file.close()
file=open("list_100.json")
json1_str = file.read()
elist=json.loads(json1_str)
file.close()
x = True
# Jaccard similarity
def jaccardSimilarity(term1,term2):
	num=len(set(term1).intersection(set(term2)))
	den=len(set(term1).union(set(term2)))
	sim_score=float(num)/float(den)
	return sim_score

# cosin similarity
def cosSimilarity(term1,term2):
	term1Set = set(term1)
	term2Set = set(terms)
	unionSet = list(term1Set + term2Set);
	a = map(lambda x: 1 if x in term1Set else 0, unionSet)
	b = map(lambda x: 1 if x in term1Set else 0, unionSet)
	return cosine(a,b)

def relevance(set1,set2):
	score_temp=0
	for i in range(len(set1)):
		for j in range(len(set2)):
			score_temp += jaccardSimilarity(word_list[set1[i]],word_list[set2[j]])
	rel_score = score_temp / (len(set1)*len(set2))

	return rel_score

def get_K(rel_score_temp):
	Threshold = threshold_otsu(rel_score_temp)
	Threshold = round(Threshold,2)
	print("Threshold:",Threshold,len(rel_score_temp))
	K = len(filter(lambda x:x > Threshold,rel_score_temp))
	return K

def get_relevance(word_list,seed_set):
	rel_score=[]
	for index in range(0,len(word_list.keys())):
		rel_score.append(relevance(seed_set,[word_list.keys()[index]]))
	return rel_score

def create_data(term_set):
	data=[]
	data_term=[]
	for term in term_set:
		data = set(data).union(set(word_list[term]))
	data = list(data)
	for index in range(0,len(data)):
		#print(index)
		data_term=set(data_term).union(set(elist[data[index]]))
	data_term=list(data_term)

	return data_term



def get_data(K,seed_set):
	data_new=seed_set
	len_data=len(data_new)
	while len(data_new) < K:
		#print(len(data_new))
		data_new = create_data(data_new)

	return data_new

def static_thresholding(data,seed_set,K):
	rel_score=[]
	R_old=[]
	R_new_temp=[]
	R_new=[]
	alpha=0.1
	for key in data.keys():
		rel_score.append(relevance(seed_set,[key]))
	sorted_term_rel = np.argsort(rel_score)[::-1]
	rel_score_temp = np.array(rel_score).round(2)
	#thresholding
	# Threshold = threshold_otsu(rel_score_temp)
	# Threshold=round(Threshold,2)
	# K=sum(rel_score_temp>=Threshold)

	for index in range(0,K):
		R_old.append(data.keys()[ sorted_term_rel[index]])

	while True:
		g_term=[]
		for index in range(0,len(data.keys())):
			sim=relevance(R_old,[data.keys()[index]])
			temp=alpha*rel_score[index]+(1-alpha)*sim
			g_term.append(temp)
		print(g_term)
		sorted_term_g = np.argsort(g_term)[::-1]
		for index in range(0,K):
			R_new.append(data.keys()[ sorted_term_g[index]])
		if (R_new!=R_old) and (set(R_new)-set(R_old)) :
			r=list(set(R_new)-set(R_old))[0]
			q=R_old[-1]
			R_new_temp=(set(R_old).union(set(r))-set(q))
			R_old=list(R_new_temp)
		else:
			R_old=R_new
			print(R_old)
			print(K)
			break




def main():
	# seed_set=raw_input("Please Enter your seed set with tab in between each seed")
	#file loading


	K_input=3
	seed_set=['galsen f olle','gals3n92','galstyle']
	data={}
	rel_score = get_relevance(word_list,seed_set)
	print(rel_score)
	sorted_term_rel = np.argsort(rel_score)[::-1]
	print(sorted_term_rel)
	rel_score_temp = np.array(rel_score).round(2)
	print(rel_score_temp)
	K = get_K(rel_score_temp)
	print("K:", K)
	data_temp = get_data(K,seed_set)
	for i in data_temp:
		data[i]=word_list[i]

	static_thresholding(data,seed_set,K)





main()
