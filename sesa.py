
file='trail.txt'
data_file= open(file, 'r')
count=0
data=[]
for line in data_file.readlines():
	# temp=line[-9:len(line)]
	# temp=temp.replace("\t","")
	# data[temp]=line[0:-9]
	#count=count+1
	data.append(line)
print(data)
print(count)
print('the count ', len(data))