COMS4705 Assignment 1
UNI: sl3766
Name: Siyao Li
Running time: PartA 1min/ PartB 15min

PartA:
2)
Command: python perplexity.py A2.uni.txt Brown_train.txt 
Result: The perplexity is 1104.83292814

Command: python perplexity.py A2.bi.txt Brown_train.txt 
Result: The perplexity is 57.2215464238

Command: python perplexity.py A2.tri.txt Brown_train.txt 
Result: The perplexity is 5.89521267642

3)
Command: python perplexity.py A3.txt Brown_train.txt 
Result: The perplexity is 13.0759217039

4)
Performance without interpolation:
I calculated the perplexity based on the uni-gram, bi-gram and tri-gram model. The perplexity of tri-gram model is the lowest. And the perplexity of bi-gram model is lower than uni-gram. Trigram model preserves more information and have better performance when predicting words on testing data. And also another important point is that we also test our model on training data, which gives the ideal testing result. If we test model on undiscovered testing data, it is likely to encounter the case of 0 frequency of tri-gram or bi-gram. And we can use interpolation to avoid this case.

Performance with interpolation:
The perplexity of interpolation is between uni-gram model and tri-gram model, because interpolation is a mix of uni-gram, bi-gram and tir-gram model. It is useful when there are 0 frequency for some trigram or bigram in the testing data. 

5)
Command: python perplexity.py Sample1_scored.txt Sample1.txt 
Result: The perplexity is 11.6492786046

Command: python perplexity.py Sample2_scored.txt Sample2.txt 
Result: The perplexity is 1611241155.03

Sample1 is more likely to belong to Brown dataset. Becaues using n-gram model trainned by Brown dataset, the perplexity of Sample1 is much lower than Sample2. So Sample1 is more similar with Brown dataset. 

PartB:
5)
Command: python pos.py B5.txt Brown_tagged_dev.txt 
Result: Percent correct tags: 93.7008827776

6)
Command: python pos.py B6.txt Brown_tagged_dev.txt 
Result: Percent correct tags: 96.9354729304

NLTK's trigram tagger with backoff has better performance than my HMM tagger. That is because trigram tagger with backoff retrieves more information about rare trigram. When we find a trigram "a b c" that has 0 frequency in training data, we still look at the bigram "b c", which also reveals some information about the trigram. However for the simple HMM model, when we find a a trigram "a b c" that has 0 frequency in training data, we simply set P(c| a b) as 0, which loses information about the trigram. So NLTK's trigram tagger with backoff has better performance than my HMM tagger.