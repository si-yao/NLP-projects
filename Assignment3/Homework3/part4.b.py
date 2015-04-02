from xml.dom import minidom
import nltk
from sklearn import svm
from sklearn import neighbors
import codecs
import sys
import unicodedata
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet as wn

def getSynset(word):
	sset = wn.synsets(word)
	sset = set(s.name().split('.')[0] for s in sset)
	return [s for s in sset]
#come into lexelt node and window size, come out train, tag data, and the maps where string mapping to the index.
#return:
#trainlist: is 2d array, each row is a vector. 
#taglist: is an array, each element corresponding to one row in trainlist.
#voca_map: word -> index in vector
#sens_map: sens_id -> tag nubmer in taglist
def extract_train_from_lex(lexnode, window, lang):
	node = lexnode
	inst_list = node.getElementsByTagName('instance')
	datalist = []
	senslist = []
	voca_set = set()
	sens_set = set()
	stemmer = SnowballStemmer(lang.lower())
	stopwords = nltk.corpus.stopwords.words(lang.lower())

	for inst in inst_list:
		l = inst.getElementsByTagName('context')[0]
		sense_id = inst.getElementsByTagName('answer')[0].getAttribute('senseid')
		if(sense_id=="U"):
			continue
		senslist.append(sense_id)
		sens_set.add(sense_id)
		#Could do stemming here.
		if(not lang.lower() == 'english'):
			l = l.getElementsByTagName('target')[0]
		before = nltk.word_tokenize((l.childNodes[0].nodeValue).replace('\n', '').lower())
		after = nltk.word_tokenize((l.childNodes[2].nodeValue).replace('\n', '').lower())
		before = [stemmer.stem(w) for w in before]# if w.lower() not in stopwords]
		after = [stemmer.stem(w) for w in after]# if w.lower() not in stopwords]
		train_dic = {}
		before_count = 0
		before_i = -1
		after_count = 0
		after_i = -1
		while(before_count<window and before_i<len(before)-1):
			before_i += 1
			voc = before[-1-before_i].lower()
			#if(len(voc)==1):
			#	continue
			lst = getSynset(voc)
			for voc in lst:
				voca_set.add(voc)
				train_dic[voc] = train_dic.get(voc,0) + 1
			before_count += 1
		while(after_count<window and after_i<len(after)-1):
			after_i += 1
			voc = after[after_i].lower()
			#if(len(voc)==1):
			#	continue
			lst = getSynset(voc);
			for voc in lst:
				voca_set.add(voc)
				train_dic[voc] = train_dic.get(voc,0) + 1
			after_count += 1
		datalist.append(train_dic)

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
		#print train 
		#raw_input("Enter!")
	for sens in senslist:
		taglist.append(sens_map[sens])

	#trainlist is 2d array, each row is a vector. taglist is an array, each element corresponding to one row in trainlist.
	#voca_map: word -> index in vector
	#sens_map: sens_id -> tag nubmer in taglist
	return (trainlist, taglist, voca_map, sens_map)


#give the lex_list, and train all the model for each lex item
#return a dic, instanceWord -> model
#for svm, para1 is gamma, para2 is C; for knn, para1 is k, para2 is weight (uniform)
def train_all(lex_list, window, alg, para1, lang):
	voca_all_map = {}
	sens_all_map = {}
	clf_map = {}
	for lex_node in lex_list:
		lexelt = lex_node.getAttribute('item')
		(trainlist, taglist, voca_map, sens_map) = extract_train_from_lex(lex_node, window, lang)
		voca_all_map[lexelt] = voca_map
		sens_all_map[lexelt] = sens_map
		if alg == 'svm':
			clf = svm.LinearSVC()
		else: #knn
			clf = neighbors.KNeighborsClassifier(para1) #para2 is usually 'uniform'
		clf.fit(trainlist, taglist)
		clf_map[lexelt] = clf
	return (clf_map, voca_all_map, sens_all_map)


def test_all_output(clf_map, voca_all_map, sens_all_map, xml_file, output, lang):
	#for k in clf_map:
	#print clf_map[k]
	#raw_input("Enter")
	data = parse_data(xml_file, lang)
	outfile = codecs.open(output, encoding = 'utf-8', mode = 'w')
	for lexelt, instances in sorted(data.iteritems(), key = lambda d: replace_accented(d[0].split('.')[0])):
		if(not lexelt in clf_map):
			continue
		for instance_id, before, after in sorted(instances, key = lambda d: int(d[0].split('.')[-1])):
			vector = get_vector_from_context(before, after, voca_all_map[lexelt], window, lang)
			#print vector
			#print before
			#print after
			#print lexelt
			#raw_input("Press Enter to continue...")
			tag = clf_map[lexelt].predict(vector)
			#print tag
			#raw_input("Enter")
			sens_map = sens_all_map[lexelt]
			for voc in sens_map:
				if sens_map[voc] == tag:
					sid = voc
					break
			outfile.write(replace_accented(lexelt + ' ' + instance_id + ' ' + sid + '\n'))
	outfile.close()


def replace_accented(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


def parse_data(input_file, lang):
	'''
	Parse the .xml dev data file

	param str input_file: The input data file path
	return dict: A dictionary with the following structure
		{
			lexelt: [(instance_id, context), ...],
			...
		}
	'''
	xmldoc = minidom.parse(input_file)
	data = {}
	lex_list = xmldoc.getElementsByTagName('lexelt')
	for node in lex_list:
		lexelt = node.getAttribute('item')
		data[lexelt] = []
		inst_list = node.getElementsByTagName('instance')
		for inst in inst_list:
			instance_id = inst.getAttribute('id')
			l = inst.getElementsByTagName('context')[0]
			if(not lang.lower() == 'english'):
				l = l.getElementsByTagName('target')[0]
			before = l.childNodes[0].nodeValue.replace('\n', '')
			after = l.childNodes[2].nodeValue.replace('\n', '')
			data[lexelt].append((instance_id, before, after))
	return data



def get_vector_from_context(before, after, voca_map, window, lang):
	stemmer = SnowballStemmer(lang.lower())
	stopwords = nltk.corpus.stopwords.words(lang.lower())
	before = nltk.word_tokenize(before.replace('\n',' ').lower())
	after = nltk.word_tokenize(after.replace('\n',' ').lower())
	before = [stemmer.stem(w) for w in before]# if w.lower() not in stopwords]
	after = [stemmer.stem(w) for w in after]# if w.lower() not in stopwords]
	size = len(voca_map)
	vector = [0 for i in range(0, size)]
	before_count = 0
	before_i = -1
	while(before_count<window and before_i<len(before)-1):
		before_i += 1
		voc = before[-1-before_count].lower()
		#if(len(voc)==1):
		#	continue
		if not voc in voca_map:
			continue
		lst = getSynset(voc)
		for voc in lst:
			vector[voca_map[voc]] += 1
		before_count += 1
	after_count = 0
	after_i = -1
	while(after_count<window and after_i<len(after)-1):
		after_i += 1
		voc = after[after_count].lower()
		#if(len(voc)==1):
		#	continue
		if not voc in voca_map:
			continue
		lst = getSynset(voc)
		for voc in lst:
			if voc in voca_map:
				vector[voca_map[voc]] += 1
		after_count += 1

	return vector

if __name__ == '__main__':
	if len(sys.argv) != 6:
		print 'Usage: python *.py [input] [output] [testfile]'
		sys.exit(0)
	lang = sys.argv[4]
	alg = sys.argv[5]
	window = 10
	xmldoc = minidom.parse(sys.argv[1])
	lex_list = xmldoc.getElementsByTagName('lexelt')
	(clf_map, voca_all_map, sens_all_map) = train_all(lex_list, window, alg, 15, lang)
	test_all_output(clf_map, voca_all_map, sens_all_map, sys.argv[3], sys.argv[2], lang)

