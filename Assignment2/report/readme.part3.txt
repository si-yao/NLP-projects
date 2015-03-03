0st feature mapping:
The feature mapping provided is not good. It has following problems:
1. lack of important features.
2. should set NULL value for words that do not have certain features. NULL is also a information, so if we just add nothing when a word does not have those feature, then we actually lose some info about the configuration.


1st feature mapping:
all of those features are set '_' by default.
stk[0]: FORM
buf[0]: FORM
buf[1]: FORM
LDEP(stk[0]): DEPREL
RDEP(stk[0]): DEPREL
LDEP(buf[0]): DEPREL
RDEP(buf[0]): DEPREL



2nd feature mapping:
all of those features are set '_' by default.
stk[0]: FORM, LEMMA, POSTAG
#stk[1]: POSTAG
LDEP(stk[0]): DEPREL
RDEP(stk[0]): DEPREL
buf[0]: FORM, LEMMA, POSTAG
buf[1]: FORM, POSTAG
buf[2]: POSTAG
buf[3]: POSTAG
LDEP(buf[0]): DEPREL
RDEP(buf[0]): DEPREL

swedish:
UAS: 0.779525990838 
LAS: 0.677952599084

korean:
UAS: 0.757821552723 
LAS: 0.640015449981

danish:
UAS: 0.769261477046 
LAS: 0.682834331337

Problem:
did not include FEATS info, which is important for danish(which has lots of additional syntax).


3rd:
stk[0]: FORM, LEMMA, POSTAG
#stk[1]: POSTAG
LDEP(stk[0]): DEPREL
RDEP(stk[0]): DEPREL
buf[0]: FORM, LEMMA, POSTAG
buf[1]: FORM, POSTAG
buf[2]: POSTAG
LDEP(buf[0]): DEPREL
RDEP(buf[0]): DEPREL
swedish, korean, danish
0.685919139614, 0.641946697567, 0.692614770459

4nd:
3rd + stk[0]:FEATS + buf[0]:FEATS
swedish, korean, danish
0.683330013941, 0.640787949015, 0.709580838323
Conclusion: stk[0]:FEATS + buf[0]:FEATS are important features for danish, which has lots of feats

5nd:
4nd + stk[1]: POSTAG
swedish, korean, danish, english
0.687114120693, 0.62495171881, 0.719760479042, 0.711111111111

