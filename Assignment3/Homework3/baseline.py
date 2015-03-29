from xml.dom import minidom
import json
import codecs
import sys
import unicodedata

def parse_data(input_file):
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
			context = (l.childNodes[0].nodeValue + l.childNodes[1].firstChild.nodeValue + l.childNodes[2].nodeValue).replace('\n', '')
			data[lexelt].append((instance_id, context))
	return data

def build_dict(language):
	'''
	Count the frequency of each sense
	'''
	data = {}
	xmldoc = minidom.parse('data/' + language + '-train.xml')
	data = {}
	lex_list = xmldoc.getElementsByTagName('lexelt')
	for node in lex_list:
		lexelt = node.getAttribute('item')
		data[lexelt] = {}
		inst_list = node.getElementsByTagName('instance')
		for inst in inst_list:
			sense_id = inst.getElementsByTagName('answer')[0].getAttribute('senseid')
			try:
				cnt = data[lexelt][sense_id]
			except KeyError:
				data[lexelt][sense_id] = 0
			data[lexelt][sense_id] += 1
	record = {}
	for key, cntDict in data.iteritems():
		sense = max(cntDict, key = lambda s: cntDict[s])
		record[key] = sense
	return record

def getFrequentSense(lexelt, sense_dict):
	'''
	Return the most frequent sense of a word (lexelt) in the training set
	'''
	sense = ''
	try:
		sense = sense_dict[lexelt]
	except KeyError:
		pass
	return sense

def replace_accented(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def most_frequent_sense(language, sense_dict):
	data = parse_data('data/' + language + '-dev.xml')
	outfile = codecs.open(language + '.baseline', encoding = 'utf-8', mode = 'w')
        for lexelt, instances in sorted(data.iteritems(), key = lambda d: replace_accented(d[0].split('.')[0])):
            for instance_id, context in sorted(instances, key = lambda d: int(d[0].split('.')[-1])):
			sid = getFrequentSense(lexelt, sense_dict)
			outfile.write(replace_accented(lexelt + ' ' + instance_id + ' ' + sid + '\n'))
	outfile.close()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: python baseline.py [language]'
		sys.exit(0)
        sense_dict = build_dict(sys.argv[1])
	most_frequent_sense(sys.argv[1], sense_dict)
