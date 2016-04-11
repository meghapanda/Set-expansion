from collections import defaultdict
import json
import gzip

debug = False
lineNum = 1000
def processBingData():
	global debug
	file='SampledWebList_SmallGraph.txt'
	data_file= open(file, 'r')
	lineCounter = 0
	data=[]
	d_word_list= defaultdict(list)
	word_list = {}
	for line in data_file:
		if debug and lineCounter >= lineNum: break
		lineCounter += 1
		line = line.split('\t')
		d_word_list[line[0]].append(line[1].strip())
		try:
			word_list[line[0]].append(line[1])
		except:
			word_list[line[0]] = [line[1]]
	if debug:
		json.dump(d_word_list, open("word_list_100.json",'w',),sort_keys=True, indent=4)
		json.dump(word_list, open("list_100.json",'w'),sort_keys=True, indent=4)
	else:
		json.dump(d_word_list, open("word_list_ALL.json",'w',),sort_keys=True, indent=4)
		json.dump(word_list, open("list_ALL.json",'w'),sort_keys=True, indent=4)
def processWikiData():
	file = "full_list_clean.txt"
	inveredTable = {}
	lineCounter = 0
	word_list = {}
	with open(file) as f:
		for line in f:
			if debug and lineCounter >= lineNum: break
			lineCounter += 1
			elems = line.split('\t')
			list_id = elems[0]
			for elem in elems[1:]:
				if elem == "": continue
				try:
					inveredTable[elem.strip()].append(list_id)
				except:
					inveredTable[elem.strip()] = [list_id]
			word_list[list_id] = elems[1:]
	with open("wiki_word_list.txt",'w+') as f:
		f.write(json.dumps(inveredTable, sort_keys=True, indent=4))
	with open("wiki_list.txt",'w+') as f:
		f.write(json.dumps(word_list, sort_keys=True, indent=4))
if __name__ == "__main__":
	processBingData()
	#processWikiData()
