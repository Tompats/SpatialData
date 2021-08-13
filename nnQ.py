#Thomas Patsanis, A.M: 3318



import sys
import ast
import math
from queue import PriorityQueue



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
def createNNQueries(nnqueries_filename):
    nnqueries_file = open(nnqueries_filename,'r')
    nnqueries = []
    query = [0,0]
    for line in nnqueries_file:
        l = line.strip('\n')
        array = l.split(' ')
        t = [float(array[0]),float(array[1])]
        nnqueries.append(t)
    return nnqueries






def getDistance(point):
    x = point[0]
    y = point[1]
    r = pow(x,2) + pow(y,2)
    result = math.sqrt(r)
    return result




def getMinimumDistance(mbr,query):
	x = query[0]
	y = query[1]
	mx_low = mbr[0]
	mx_high = mbr[1]
	my_low = mbr[2]
	my_high = mbr[3]
	dx = 0
	dy = 0
	if x<mx_low:
		dx = mx_low - x
	elif x>mx_high:
		dx = x - mx_high
	else:
		dx = 0
	if y<my_low:
		dy = my_low - y
	elif y>my_high:
		dy = y - my_high
	else:
		dy = 0
	point = [dx,dy]
	min_dist = getDistance(point)
	return min_dist




def isInside(mbr,query):
	if query[0]>=mbr[0] and query[0]<= mbr[1]:
		if query[1]>=mbr[2] and query[1]<= mbr[3]:
			return True
	return False



def bf_NN_Queries(tree,rootId,query,k):
	inf_array = [-math.inf,0]
	results_array = []
	counter = 0
	q = PriorityQueue()
	value = tree[rootId]
	isnonleaf = value[0]
	children = value[1]
	for child in children:
		child_dist = getMinimumDistance(child[1],query)
		q.put([child_dist,child])
	while not q.empty():
		node = q.get()[1]
		if not isinstance(node,list):
			results_array.append(node)
			counter+=1
			if counter==k:
				break
			else:
				continue
		value = tree[node[0]]
		isnonleaf = value[0]
		children = value[1]
		if isnonleaf==1:
			for child in children:
				child_dist = getMinimumDistance(child[1],query)
				q.put([child_dist,child])
		elif isnonleaf==0:
			for child in children:
				child_dist = getMinimumDistance(child[1],query)
				childId = child[0]
				q.put([child_dist,childId])
	return results_array





#get result for every query
def findResults(tree,nnqueries,k):
    rootId = getRootId(tree)
    line = 0
    str_array = []
    results = []
    for query in nnqueries:
        results = bf_NN_Queries(tree,rootId,query,k)
        s = str(line)+": "+toString(results)
        print(s)
        str_array.append(s)
        line += 1
    return str_array






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




def writeResults(str_array):
	file = open('NNQueries_Results.txt', 'w')
	for i in str_array:
		file.write(i+"\n")





def main(argv):
    rtree_filename = argv[0]
    nnqueries_filename = argv[1]
    k = int(argv[2])
    tree = readRTree(rtree_filename)
    nnqueries = createNNQueries(nnqueries_filename)
    str_array = findResults(tree,nnqueries,k)
    writeResults(str_array)


if __name__ == '__main__':
	main(sys.argv[1:])
