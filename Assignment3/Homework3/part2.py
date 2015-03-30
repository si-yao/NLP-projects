from xml.dom import minidom
import nltk
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

if __name__ == '__main__':
	xmldoc = minidom.parse('lexnode.xml')
	lex_node = xmldoc.getElementsByTagName('lexelt')[0]
	(trainlist, taglist, voca_map, ses_map) = extract_train_from_lex(lex_node, 10)
	print trainlist
	print taglist
	

