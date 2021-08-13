#Thomas Patsanis, A.M: 3318

import sys

#from github
_DIVISORS = [180.0 / 2 ** n for n in range(32)]


#from github
def interleave_latlng(lat, lng):
    if not isinstance(lat, float) or not isinstance(lng, float):
        print('Usage: interleave_latlng(float, float)')
        raise ValueError("Supplied arguments must be of type float!")

    if (lng > 180):
        x = (lng % 180) + 180.0
    elif (lng < -180):
        x = (-((-lng) % 180)) + 180.0
    else:
        x = lng + 180.0
    if (lat > 90):
        y = (lat % 90) + 90.0
    elif (lat < -90):
        y = (-((-lat) % 90)) + 90.0
    else:
        y = lat + 90.0

    morton_code = ""
    for dx in _DIVISORS:
        digit = 0
        if (y >= dx):
            digit |= 2
            y -= dx
        if (x >= dx):
            digit |= 1
            x -= dx
        morton_code += str(digit)

    return morton_code



#read files and create objects with their id and mbr
def createMBRS(coords_filename,offsets_filename):
	coords_file = open(coords_filename, 'r')
	offsets_file = open(offsets_filename, 'r')
	offsets = []
	objects = []
	for line in offsets_file:
		offsets = line.split(',')
		mbr_id = int(offsets[0])
		start = int(offsets[1])
		end = int(offsets[2])+1
		array_x = []
		array_y = []
		for i in range(start,end):
			str_coords = coords_file.readline()
			coords = str_coords.split(',')
			array_x.append(float(coords[0]))
			array_y.append(float(coords[1]))
		x_low = min(array_x)
		x_high = max(array_x)
		y_low = min(array_y)
		y_high = max(array_y)
		mbr = [mbr_id,[x_low,x_high,y_low,y_high]]
		objects.append(mbr)
	coords_file.close()
	offsets_file.close()
	return objects





#returns a string based on mbr's center
def getZ(mbr):
	avg_x = (mbr[0]+mbr[1]) / 2
	avg_y = (mbr[2] + mbr[3]) / 2
	z = interleave_latlng(avg_y,avg_x)
	return z



#return objects sorted by z-order
def sortMBR(objects_array):
	z_array = []
	sorted_objects = []
	for object in objects_array:
		mbr = object[1]
		z = getZ(mbr)
		z_array.append([z,object])
	z_array.sort()
	for i in z_array:
		sorted_objects.append(i[1])
	return sorted_objects









def createNode(leaf):
	x_array = []
	y_array = []
	for i in leaf:
		x_array.append(i[-1][0])
		x_array.append(i[-1][1])
		y_array.append(i[-1][2])
		y_array.append(i[-1][3])
	node = [min(x_array),max(x_array),min(y_array),max(y_array)]
	return node









def createRTree(nodes,counter_node,counter_level,tree,isnonleaf):
	nodes_in_each_level = 0
	new_nodes = []
	n = len(nodes)
	k = 0
	for i in range(0,n,20):
		k+=20
		leaf_nodes = nodes[i:k]
		if(len(leaf_nodes)<8) and nodes_in_each_level>=1:
			size = 8 - len(leaf_nodes)
			for i in tree[-1][-1][len(tree[-1][-1])-size:]:
				leaf_nodes.append(i)
				tree[-1][-1].remove(i)
			leaf_nodes.sort()
		record = [isnonleaf,counter_node,leaf_nodes]
		tree.append(record)
		nodes_in_each_level += 1
		new_nodes.append([counter_node,createNode(leaf_nodes)])
		counter_node += 1
	print(str(nodes_in_each_level)+' nodes at level '+str(counter_level))
	counter_level += 1
	nodes_in_each_level = 0
	if(len(new_nodes))>1:
		createRTree(new_nodes,counter_node,counter_level,tree,1)
	return tree





def writeTreeToFile(tree):
	file = open('Rtree.txt', 'w')
	for i in tree:
		file.write(str(i)+"\n")
	file.close()



def main(argv):
	coords_filename = argv[0]
	offsets_filename = argv[1]
	objects_array = []
	sorted_objects_array = []
	tree = []
	objects_array = createMBRS(coords_filename,offsets_filename)
	sorted_objects_array = sortMBR(objects_array)
	tree = createRTree(sorted_objects_array,0,0,[],0)
	writeTreeToFile(tree)



if __name__ == '__main__':
	main(sys.argv[1:])
