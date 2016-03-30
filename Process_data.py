from collections import defaultdict
import json
import gzip

file='SampledWebList_SmallGraph.txt'
#file='trail.txt'
data_file= open(file, 'r')
lineNum = 100
lineCounter = 0
data=[]
d_word_list= defaultdict(list)
for line in data_file:
	if lineCounter >= lineNum: break
	lineCounter += 1
	line = line.split('\t')
	d_word_list[line[0]].append(line[1].strip())

json.dump(d_word_list, open("word_list_100.json",'w',),sort_keys=True, indent=4)
json.dump(d_word_list.keys(), open("list_100.json",'w'),sort_keys=True, indent=4)
