from providedcode.transitionparser import TransitionParser
from providedcode.dependencygraph import DependencyGraph
import fileinput
# parsing arbitrary sentences (english):

for line in fileinput.input():

    sentence = DependencyGraph.from_sentence(line)
    tp = TransitionParser.load('english.model')
    parsed = tp.parse([sentence])
    print parsed[0].to_conll(10).encode('utf-8')