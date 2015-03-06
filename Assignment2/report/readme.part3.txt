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

>>>>>>>>>>>>>>
a)
The feature mapping provided by default is not good. It has following problems:
1. lack of important features.
2. should set NULL value for words that do not have certain features. NULL is also a information, so if we just add nothing when a word does not have those feature, then we actually lose some info about the configuration.


I added few more features shown as follows:
stk[0]: FORM, LEMMA, POSTAG, CPOSTAG, FEATS, NUM_OF_LEFT_CHILD, NUM_OF_RIGHT_CHILD
stk[1]: POSTAG, CPOSTAG
LDEP(stk[0]): DEPREL
RDEP(stk[0]): DEPREL
buf[0]: FORM, LEMMA, POSTAG, CPOSTAG, FEATS, NUM_OF_LEFT_CHILD, NUM_OF_RIGHT_CHILD
buf[1]: FORM, POSTAG, CPOSTAG
buf[2]: POSTAG, CPOSTAG
LDEP(buf[0]): DEPREL
RDEP(buf[0]): DEPREL

Above, FORM, LEMMA, POSTAG, CPOSTAG, FEATS are the features provided by CoNLL. And NUM_OF_LEFT_CHILD, NUM_OF_RIGHT_CHILD are the number of left children and the number of right children respectively. LDEP(node) is the left most dependence of a certain node, and RDEP(node) is the right most dependence of a certain node. DEPREL is the relation on a certain dependence.

The performance(LAS) of 4 language towards testing data is: (English is evaluated by dev data)
Swedish: 0.676359290978
Korean: 0.63460795674
Danish: 0.710978043912
English: 0.713580246914



Discussion of some features:
*FEATS of stk[0], buf[0]
FEATS is additional syntactic features of a certain word. By examining the training data, I noticed that Danish has lots of additional syntactic features. So I guess it might be very helpful for adding this features. After add this feature, the LAS of Danish increases 2%. I read FEATS from the training data directly. So the complexity is O(1).

*CPOSTAG of stk[0], buf[0], buf[1], buf[2]
CPOSTAG is the universal POS tag, as known as simplified tag. In the testing, I found that CPOSTAG is very helpful for English model, increasing the LAS for 1%. I guess the reason is that English has lots of detailed tags defined in POSTAG, but most of them have similar feature in syntactic level. So, if we use CPOSTAG as an feature, then we could provide svm a better guide for the syntacitc feature of English. I read CPOSTAG from the training data directly. So the complexity is O(1).

*NUM_OF_LEFT_CHILD, NUM_OF_RIGHT_CHILD of stk[0] and buf[0]
Number of children is a good feature for Korean model. It increases the performance for Korean by 0.5%. After visualize the dependence graph, I found that Korean has a very special property. In Korean, the head is usually at the right side pointing to the left side. And most of node has only 1 dependence. And also has few nodes has 2 or more dependence, which could be important nodes from my speculation. So, this feature could be helpful for identifying those important nodes. To count the number of children of a certain node, I traverse all dependencies in "arcs" and count. The complexity to extract the feature for one state is O(n), where n is the number of dependencies. 

*POSTAG of stk[1]
This feature is helpful for all languages. It increases the performance of Swedish, Korean, Danish and English by 0.4%, 0.5%, 1% and 1$ respectively. I read POSTAG from the training data directly. So the complexity is O(1).


d)????????????????????????the complexity of the arc-eager shift-reduce parser, and what tradeoffs it makes.


