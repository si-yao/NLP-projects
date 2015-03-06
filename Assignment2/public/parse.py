from providedcode.transitionparser import TransitionParser
from providedcode.dependencygraph import DependencyGraph
import fileinput
import sys
# parsing arbitrary sentences (english):
import nltk
from nltk.tag.simplify import simplify_wsj_tag
if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print "need 1 argument for model!"
        exit(1)

    tp = TransitionParser.load(sys.argv[1])
    line = sys.stdin.readline()
    while line:
        tokens = nltk.word_tokenize(line)
        tagged = nltk.pos_tag(tokens)
        sentence = DependencyGraph.from_sentence(line)
        for (index, (word, tag)) in enumerate(tagged):
            sentence.nodes[index + 1]['ctag'] = tag

        parsed = tp.parse([sentence])
        print parsed[0].to_conll(10).encode('utf-8')
        line = sys.stdin.readline()