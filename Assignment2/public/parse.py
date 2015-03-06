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

    for line in fileinput.input():
            sentence = DependencyGraph.from_sentence(line)
            for node in sentence.nodes:
                node['ctag'] = '_'

            parsed = tp.parse([sentence])
            print parsed[0].to_conll(10).encode('utf-8')