import json
import numpy as np
from skimage.filters import threshold_otsu
import math
import timeit
from scipy.spatial.distance import cosine,jaccard
import multiprocessing as mp
from multiprocessing import Pool
file = open("word_list_ALL.json")
json1_str = file.read()
word_list=json.loads(json1_str)
file.close()
file=open("list_ALL.json")
json1_str = file.read()
elist=json.loads(json1_str)
file.close()
print('data Reading Done')
x = True
# Jaccard similarity
def jaccardSimilarity(term1,term2):
	term1Set = set(term1)
	term2Set = set(term2)
	unionSet = list(term1Set.union(term2Set));
	a = map(lambda x: 1 if x in term1Set else 0, unionSet)
	b = map(lambda x: 1 if x in term1Set else 0, unionSet)
	return jaccard(a,b)

# cosin similarity
def cosSimilarity(term1,term2):
	term1Set = set(term1)
	term2Set = set(terms)
	unionSet = list(term1Set + term2Set);
	a = map(lambda x: 1 if x in term1Set else 0, unionSet)
	b = map(lambda x: 1 if x in term1Set else 0, unionSet)
	return cosine(a,b)



def similarity(term1,term2):
	num=len(set(term1).intersection(set(term2)))
	den=len(set(term1).union(set(term2)))
	sim_score=float(num)/float(den)
	return sim_score


def relevance(set1,set2):
	len_set1=len(set1)
	len_set2=len(set2)
	score_temp = 0.0
	for i in set1:
		a = word_list[i]
		socre_list = map(lambda x:jaccardSimilarity(a,word_list[x]),set2)
		score_temp += sum(socre_list)
	rel_score = score_temp / (len_set1 * len_set1)
	return rel_score



def get_K(seed_set):
	print("Begin Get K")
	rel_score=[]
	p = Pool(8)
	#def g(x,y = seed_set):
	#	return relevance(y,x)
	#rel_score = p.map(g, word_list.keys())
	for index in range(0,len(word_list.keys())):
		print(str(index)+"/" +str(len(word_list.keys())))
		rel_score.append(relevance(seed_set,[word_list.keys()[index]]))
	rel_score_temp=np.array(rel_score).round(2)
	Threshold = threshold_otsu(rel_score_temp)
	Threshold=round(Threshold,2)
	print('Threashold',Threshold)
	K=sum(rel_score_temp>=Threshold)
	print(K)
	return K

def create_data(term_set):
	data=[]
	data_term=[]
	for index in range(0,len(term_set)):
		data=set(data).union(set(word_list[term_set[index]]))
	data=list(data)
	for index in range(0,len(data)):
		data_term=set(data_term).union(set(elist[data[index]]))
	data_term=list(data_term)

	return data_term

def get_data(K,seed_set):
	data_new=seed_set
	len_data=len(data_new)
	while K > len(data_new):
		len_data=len(data_new)
		data_new=create_data(data_new)
		if (len(data_new)==len_data):
			K=len_data
			print('len',len_data)
			break;
	return data_new,K

def static_thresholding(data,seed_set,K):

	rel_score=[]
	R_old=[]
	R_new_temp=[]
	R_new=[]
	alpha=0.1
	for index in range(0,len(data.keys())):
		rel_score.append(relevance(seed_set,[data.keys()[index]]))
	sorted_term_rel = np.argsort(rel_score)[::-1]

	for index in range(0,K):
		R_old.append(data.keys()[ sorted_term_rel[index]])

	while True:
		g_term=[]
		for index in range(0,len(data.keys())):
			sim=relevance(R_old,[data.keys()[index]])
			temp=alpha*rel_score[index]+(1-alpha)*sim
			g_term.append(temp)

		sorted_term_g = np.argsort(g_term)[::-1]
		for index in range(0,K):
			R_new.append(data.keys()[ sorted_term_g[index]])
		if (R_new!=R_old) and (set(R_new)-set(R_old))  :
			r = list(set(R_new)-set(R_old))[0]
			q = R_old[-1]
			R_new_temp = (set(R_old).union(set(r))-set(q))
			R_old=list(R_new_temp)
		else:
			R_old=R_new
			break
	return R_old




def main():
	# seed_set=raw_input("Please Enter your seed set with tab in between each seed")
	K_input=2
	seed_set = ["country"]
	K=get_K(seed_set)
	data_temp=get_data(K,seed_set)
	K=data_temp[1]
	for i in data_temp[0]:
		data[i]=word_list[i]
	t0=time.time()
	expanded=static_thresholding(data,seed_set,K)
	t1 = time.time()
	total = t1-t0
	print(expanded)
	print('Total Time taken',total)



main()
