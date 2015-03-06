from providedcode.transitionparser import TransitionParser
from providedcode.dependencygraph import DependencyGraph
import fileinput
import sys
# parsing arbitrary sentences (english):

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print "need 1 argument for model!"
        exit(1)

    tp = TransitionParser.load(sys.argv[1])
    line = sys.stdin.readline()
    while line:
            sentence = DependencyGraph.from_sentence(line)
            for (index, node) in enumerate(sentence.nodes):
                sentence.nodes[index]['ctag'] = '_'

            parsed = tp.parse([sentence])
            print parsed[0].to_conll(10).encode('utf-8')
            line = sys.stdin.readline()