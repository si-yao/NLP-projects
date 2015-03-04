from providedcode.transitionparser import TransitionParser
from providedcode.evaluate import DependencyEvaluator
from featureextractor import FeatureExtractor
from transition import Transition
# parsing arbitrary sentences (english):
sentence = DependencyGraph.from_sentence('Hi, this is a test')

tp = TransitionParser.load('english.model')
parsed = tp.parse([sentence])
print parsed[0].to_conll(10).encode('utf-8')