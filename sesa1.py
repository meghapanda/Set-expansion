import json
import numpy as np
from skimage.filters import threshold_otsu
import math
from timer import Timer
from redis import Redis
rdb = Redis()

def similarity(term1,term2):
	num=len(set(term1).intersection(set(term2)))
	den=len(set(term1).union(set(term2)))
	sim_score=float(num)/float(den)
	return sim_score


def relevance(set1,set2):
	len_set1=len(set1)
	len_set2=len(set2)
	score_temp=0
	for i in range(0,len_set1):
		for j in range(0,len_set2):
			score_temp=score_temp+similarity(data[set1[i]],data[set2[j]])
	rel_score=score_temp/(len_set1*len_set1)

	return rel_score


#@profile
def static_thresholding(data,seed_set):
	rel_score=[]
	R_old=[]
	R_new_temp=[]
	R_new=[]
	alpha=1
	for index in range(0,len(data.keys())):
		rel_score.append(relevance(seed_set,[data.keys()[index]]))
	sorted_term_rel = np.argsort(rel_score)[::-1]
	rel_score_temp=np.array(rel_score).round(2)
	#thresholding
	Threshold = threshold_otsu(rel_score_temp)
	Threshold=round(Threshold,2)
	K=sum(rel_score_temp>=Threshold)

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
		if (R_new!=R_old) and (set(R_new)-set(R_old)) :
			print('j')
			r=list(set(R_new)-set(R_old))[0]
			q=R_old[-1]
			R_new_temp=(set(R_old).union(set(r))-set(q))
			R_old=list(R_new_temp)
		else:
			R_old=R_new
			print(R_old)
			print(K)
			break







#main part
file=open("word_list.txt")
json1_str = file.read()
data=json.loads(json1_str)

# seed_set=raw_input("Please Enter your seed set with tab in between each seed")
seed_set='a\tg'
seed_set=seed_set.split("\t")
static_thresholding(data,seed_set)
