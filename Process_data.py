from collections import defaultdict
import json
import gzip

debug = False
def processBingData():
	file='SampledWebList_SmallGraph.txt'
	data_file= open(file, 'r')
	lineNum = 100
	lineCounter = 0
	data=[]
	d_word_list= defaultdict(list)
	for line in data_file:
		if debug and lineCounter >= lineNum: break
		lineCounter += 1
		line = line.split('\t')
		d_word_list[line[0]].append(line[1].strip())
	if DEBUG:
		json.dump(d_word_list, open("word_list_100.json",'w',),sort_keys=True, indent=4)
		json.dump(d_word_list.keys(), open("list_100.json",'w'),sort_keys=True, indent=4)
	else:
		json.dump(d_word_list, open("word_list_ALL.json",'w',),sort_keys=True, indent=4)
		json.dump(d_word_list.keys(), open("list_ALL.json",'w'),sort_keys=True, indent=4)
def processWikiData():
	file = "full_list_clean.txt"
	inveredTable = {}
	with open(file) as f:
		for line in f:
			elems = line.split('\t')
			list_id = elems[0]
			for elem in elems[1:]:
				if elem == "": continue
				try:
					inveredTable[list_id].append(elem.strip())
				except:
					inveredTable[list_id] = [elem.strip()]
	with open("full_list_inverted_table.txt",'w+') as f:
		f.write(json.dumps(inveredTable,sort_keys=True, indent=4))
if __name__ == "__main__":
	processWikiData()
