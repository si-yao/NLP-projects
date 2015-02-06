import nltk as nl
from nltk.corpus import brown
sentence = "It's 3 AM in the morning, I put my key in the door. There's bodies laying all of the floor."
news_sents = "<S> One suggestion would even involve selling or perhaps redeveloping the organization's Washington quarters, which is on prime real estate near the White House. Under tightened government ethics rules, the building's screening room, though still active, is no longer the scene of lavish movie-and-dinner nights that were once popular with lawmakers. </S>"

sentence = news_sents
tokens = nl.word_tokenize(sentence)
print tokens
"""
bigram_tuples = tuple(nl.bigrams(tokens))
trigram_tuples = tuple(nl.trigrams(tokens))

print bigram_tuples
print trigram_tuples

count = len(bigram_tuples)
print count

count = {item : bigram_tuples.count(item) for item in set(bigram_tuples)}
print count

default_tagger = nl.DefaultTagger('NN')
tagged_sentence = default_tagger.tag(tokens)
print tagged_sentence


patterns = [(r'.*ing$', 'VBG'),(r'.*ed$', 'VBD'),(r'.*es$', 'VBZ'),(r'.*ed$', 'VB')] 
regexp_tagger = nl.RegexpTagger(patterns)
tagged_sentence = regexp_tagger.tag(tokens)
print tagged_sentence
"""

training = brown.tagged_sents(categories='news')
#print training
def_tagger = nl.DefaultTagger('NN')
uni_tagger = nl.UnigramTagger(training, backoff=def_tagger)
bi_tagger = nl.BigramTagger(training, backoff=uni_tagger)
tri_tagger = nl.TrigramTagger(training, backoff=bi_tagger)

print uni_tagger.tag(tokens)
print bi_tagger.tag(tokens)
print tri_tagger.tag(tokens)



