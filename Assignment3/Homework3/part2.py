from xml.dom import minidom
import nltk
from sklearn import svm
from sklearn import neighbors
#come into lexelt node and window size, come out train, tag data, and the maps where string mapping to the index.
#return:
#trainlist: is 2d array, each row is a vector. 
#taglist: is an array, each element corresponding to one row in trainlist.
#voca_map: word -> index in vector
#sens_map: sens_id -> tag nubmer in taglist
def extract_train_from_lex(lexnode, window):
	node = lexnode
	inst_list = node.getElementsByTagName('instance')
	datalist = []
	senslist = []
	voca_set = set()
	sens_set = set()
	for inst in inst_list:
		l = inst.getElementsByTagName('context')[0]
		#Could do stemming here.
		before = nltk.word_tokenize((l.childNodes[0].nodeValue).replace('\n', ''))
		after = nltk.word_tokenize((l.childNodes[2].nodeValue).replace('\n', ''))
		train_dic = {}
		for i in range(0,window):
			if i<len(before):
				voc = before[-1-i]
				voca_set.add(voc)
				train_dic[voc] = train_dic.get(voc,0) + 1
			if i<len(after):
				voc = after[i]
				voca_set.add(voc)
				train_dic[voc] = train_dic.get(voc,0) + 1
		datalist.append(train_dic)
		sense_id = inst.getElementsByTagName('answer')[0].getAttribute('senseid')
		senslist.append(sense_id)
		sens_set.add(sense_id)
	voca_map = {}
	train_idx = 0
	for voc in voca_set:
		voca_map[voc] = train_idx
		train_idx += 1
	sens_map = {}
	sens_idx = 0
	for sens in sens_set:
		sens_map[sens] = sens_idx
		sens_idx += 1

	trainlist = []
	taglist = []
	for data_dic in datalist:
		train = [ 0 for i in range(0,train_idx)]
		for voc in data_dic:
			train[voca_map[voc]] += data_dic[voc]
		trainlist.append(train)
	for sens in senslist:
		taglist.append(sens_map[sens])

	#trainlist is 2d array, each row is a vector. taglist is an array, each element corresponding to one row in trainlist.
	#voca_map: word -> index in vector
	#sens_map: sens_id -> tag nubmer in taglist
	return (trainlist, taglist, voca_map, sens_map)


#give the lex_list, and train all the model for each lex item
#return a dic, instanceWord -> model
#for svm, para1 is gamma, para2 is C; for knn, para1 is k, para2 is weight (uniform)
def train_all(lex_list, alg, para1, para2):
	voca_all_map = {}
	sens_all_map = {}
	clf_map = {}
	for lex_node in lex_list:
		lexelt = lex_node.getAttribute('item')
		(trainlist, taglist, voca_map, sens_map) = extract_train_from_lex(lex_node, 10)
		voca_all_map[lexelt] = voca_map
		sens_all_map[lexelt] = sens_map
		if alg == 'svm':
			clf = svm.SVC(gamma=para1, C=para2)
		else: #knn
			clf = neighbors.KNeighborsClassifier(para1, weights=para2) #para2 is usually 'uniform'
		clf.fit(trainlist, taglist)
		clf_map[lexelt] = clf
	return (clf_map, voca_all_map, sens_all_map)

def test_all_output(clf_map, voca_all_map, sens_all_map, xml_file, output):
	data = parse_data(xml_file)
	outfile = codecs.open(output, encoding = 'utf-8', mode = 'w')
	for lexelt, instances in sorted(data.iteritems(), key = lambda d: replace_accented(d[0].split('.')[0])):
		if(not lexelt in clf_map):
			continue
		for instance_id, context in sorted(instances, key = lambda d: int(d[0].split('.')[-1])):
			vector = get_vector_from_context(context, voca_all_map[lexelt], 10)
			tag = clf_map[lexelt].predict(vector)
			sens_map = sens_all_map[lexelt]
			for voc in sens_map:
				if sens_map[voc] == tag:
					sid = voc
					break
			outfile.write(replace_accented(lexelt + ' ' + instance_id + ' ' + sid + '\n'))
	outfile.close()

def get_vector_from_context(context_node, voca_map, window):
		before = nltk.word_tokenize((context_node.childNodes[0].nodeValue).replace('\n', ''))
		after = nltk.word_tokenize((context_node.childNodes[2].nodeValue).replace('\n', ''))
		size = len(voca_map)
		vector = [0 for i in range(0, size)]
		for i in range(0, window):
			if(i < len(before)):
				if(before[-1-i] in voca_map):
					vector[voca_map[before[-1-i]]] += 1
			if(i < len(after)):
				if(after[i] in voca_map):
					vector[voca_map[after[i]]] += 1
		return vector

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Usage: python *.py [input] [output] [testfile]'
		sys.exit(0)
	xmldoc = minidom.parse(sys.argv[1])
	lex_list = xmldoc.getElementsByTagName('lexelt')
	(clf_map, voca_all_map, sens_all_map) = train_all(lex_list, 'svm', 0.001, 100)
	test_all_output(clf_map, voca_all_map, sens_all_map, sys.argv[3], sys.argv[2])

