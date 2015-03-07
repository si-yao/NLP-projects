Name: Siyao Li
UNI: sl3766
---------------------------------
1.
b)
For every dependency, (i,j), having i<j, one is the head, and one is the child, search every node pairs (y,z) where i<y<j, and z<i or z>j, if the dependence (y,z) exist in the graph, then it is non-projective and return false. After searching every pairs and did not return false, then the graph is projective, and return true.

c)
example that is projective:
I drink teas rather than coffee.
Parsing result:
nsubj(drink-2, I-1)
root(ROOT-0, drink-2)
dobj(drink-2, teas-3)
cc(teas-3, rather-4)
mwe(rather-4, than-5)
conj(teas-3, coffee-6)

example that is non-projective:
What I said is used by him.
Parsing result:
dobj(said-3, What-1)
nsubjpass(used-5, What-1)
nsubj(said-3, I-2)
root(ROOT-0, said-3)
auxpass(used-5, is-4)
ccomp(said-3, used-5)
agent(used-5, him-7)


---------------------------------
2.
b)
The performance of the parser using badfeatures.model is shown as follows:
swedish
UAS: 0.229038040231 
LAS: 0.125473013344
korean
UAS: 0.115488605639 
LAS: 0.0
danish
UAS: 0.123552894212 
LAS: 0.00718562874251
english
UAS: 0.0518518518519 
LAS: 0.0

From the result we could see the badfeatures.model has poor performance for all of the languages. And also we could see that for Swedish, it has 0.125 accuracy, while for other language, it has nearly 0 accuracy. So I can conclude that this model is trained by Swedish sentences. 

The possible reason for the poor performance is because it did not select useful features in the training part. The model is very likely trained by the sample code provided in featureextractor.py. The feature selection in featureextractor.py has 2 main problems. 1) lack of important features. 2) should set NULL value for words that do not have certain features. NULL is also a information, so if we just add nothing when a word does not have those feature, then we actually lose some information about the configuration.


---------------------------------
3.
a)
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

Above, FORM, LEMMA, POSTAG, CPOSTAG, FEATS are the features provided by CoNLL. And NUM_OF_LEFT_CHILD, NUM_OF_RIGHT_CHILD are the number of left children and the number of right children respectively. LDEP(node) is the left most dependence of a certain node, and RDEP(node) is the right most dependence of a certain node. DEPREL is the relation on a certain dependency.

The performance(LAS) of 4 language towards testing data: (English is evaluated by dev data)
Swedish: 0.676359290978
Korean: 0.63460795674
Danish: 0.710978043912
English: 0.713580246914


Discussion of some features:
*
FEATS of stk[0], buf[0]
FEATS is additional syntactic features of a certain word. By examining the training data, I noticed that Danish has lots of additional syntactic features. So I guess it might be very helpful for adding this features. After add this feature, the LAS of Danish increases 2%. I read FEATS from the training data directly. So the complexity is O(1).

*
CPOSTAG of stk[0], buf[0], buf[1], buf[2]
CPOSTAG is the universal POS tag, as known as simplified tag. In the testing, I found that CPOSTAG is very helpful for English model, increasing the LAS for 1%. I guess the reason is that English has lots of detailed tags defined in POSTAG, but most of them have similar feature in syntactic level. So, if we use CPOSTAG as an feature, then we could provide svm a better guide for the syntacitc feature of English. I read CPOSTAG from the training data directly. So the complexity is O(1).

*
NUM_OF_LEFT_CHILD, NUM_OF_RIGHT_CHILD of stk[0] and buf[0]
Number of children is a good feature for Korean model. It increases the LAS for Korean by 0.5%. After visualize the dependency graph, I found that Korean has a very special property. In Korean, the head is usually at the right side pointing to the left side. And most of node has only 1 dependence. And also those nodes that have 2 or more dependence could be important nodes from my speculation. So, this feature could be helpful for identifying those important nodes. To count the number of children of a certain node, I traverse all dependencies in "arcs" and count. The complexity to extract the feature for one state is O(n), where n is the number of dependencies. 

*
POSTAG of stk[1]
This feature is helpful for all languages. It increases the LAS of Swedish, Korean, Danish and English by 0.4%, 0.5%, 1% and 1% respectively. I read POSTAG from the training data directly. So the complexity is O(1).


d)
The complexity of the classic (without SVM) arc-eager shift-reduce parser is O(N), where N is the number of words of a sentence. The parser reads words one by one from left to right, and create dependency as soon as possible.

If we consider the complexity of extracting features and SVM, then the complexity could be much higher. First extracting features from one configuration need O(N) operations. And for each sentence, it at most has N configurations, so the complexity for extracting features for a sentence is O(N^2). And if we have M training datas, then we need O(MN^2) operations for extracting features. Moreover, the complexity of SVM could be much higher, which depends on the implementation of SVM. 

The algorithm has some tradoffs. The first one is that the algorithm only works for projective sentences. And second, if the algorithm reaches the configuration that cannot derive the gold tree, then the accuracy of the result will be low. 




