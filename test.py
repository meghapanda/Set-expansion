import json
print('start ')
file=open("word_list.txt")
json1_str = file.read()
a=json.loads(json1_str)
print (len(a))