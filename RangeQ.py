#Thomas Patsanis, A.M: 3318


import sys
import ast



#return the Rtree
def readRTree(rtree_filename):
	rtree_file = open(rtree_filename, 'r')
	rtree = {}
	for line in rtree_file:
		array = ast.literal_eval(line)
		#rtree.insert(0,array)
		key = array[1]
		isnonleaf = array[0]
		children = array[2:]
		children.insert(0,isnonleaf)
		value =  children
		rtree[key] = value
	#print(rtree)
	return rtree



#Return an array with all the Rqueries
def createRQueries(rqueries_filename):
	rqueries_file = open(rqueries_filename,'r')
	rqueries = []
	query = [0,0,0,0]
	for line in rqueries_file:
		l = line.strip('\n')
		array = l.split(' ')
		t = [float(array[0]),float(array[2]),float(array[1]),float(array[3])]
		rqueries.append(t)
	#print(rqueries)
	return rqueries




#Find mbrs that intersect query
def inRange(tree,nodeId,query,results):
	value = tree[nodeId]
	isnonleaf = value[0]
	#print(isnonleaf)
	children = value[1]
	#if node is not a leaf
	if isnonleaf == 1:
		for child in children:
			n_id = child[0]
			mbr = child[1]
			#print(n_id)
			if(filter(mbr,query)):# or filter(query,mbr)):
				inRange(tree,n_id,query,results)
	elif isnonleaf == 0:
		for child in children:
			n_id = child[0]
			mbr = child[1]
			if(filter(mbr,query)):# or filter(query,mbr)):
				#print(n_id)
				results.append(n_id)





def filter(mbr,query):
	x_low = query[0]
	x_high = query[1]
	y_low = query[2]
	y_high = query[3]
	counter = 0
	if((x_low>=mbr[0] and x_low<= mbr[1]) or (x_low<=mbr[0] and x_high>= mbr[0])):
		counter+=1
	if((y_low>=mbr[2] and y_low<= mbr[3]) or (y_low<=mbr[2] and y_high>= mbr[2])):
		counter+=1
	if(counter == 2):
		return True
	return False





def getRootId(tree):
	lst = list(tree.items())
	root = lst[-1][0]
	return root




def toString(array):
	string = ""
	for i in range(len(array)):
		if i==len(array)-1:
			string += str(array[i])
		else:
			string += str(array[i])+','
	return string



#get result for every query
def findResults(tree,rqueries):
	rootId = getRootId(tree)
	line = 0
	str_array = []
	for query in rqueries:
		results = []
		inRange(tree,rootId,query,results)
		s = str(line)+" ("+str(len(results))+"): "+toString(results)
		print(s)
		str_array.append(s)
		line += 1
	return str_array




def writeResults(str_array):
	file = open('RangeQueries_Results.txt', 'w')
	for i in str_array:
		file.write(i)





def main(argv):
	rtree_filename = argv[0]
	rqueries_filename = argv[1]
	tree = readRTree(rtree_filename)
	rqueries = createRQueries(rqueries_filename)
	str_array = findResults(tree,rqueries)



if __name__ == '__main__':
	main(sys.argv[1:])
