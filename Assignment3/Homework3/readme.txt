Name: Siyao Li
UNI: sl3766

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Note:
For all the result shown in the following, I use some symbols and notations for simplicity.
Here, "eng", "spa", "cat" represents English, Spanish and Catalan respectively. 
And the precision of svm and knn classifier for each language follows the language name.
Because the recall always equals to the precision, *I simply use one number to represent both*.
And "+" notation means I took some methods into consideration. 
For example, "+stopwords" means I removed stopwords, and "+stemming" means I did stemming.
And the indent in each "+" means I did something after somthing.
For example, 
+stopwords
	+stemming
		.....
, the result in ..... means I did the stemming after removing stopwords.


>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Part2:
I trained classifiers for SVM and KNN. I use window size 10, and did not ignore any special characters.
The result is shown as follows:

window = 10
	eng: svm 0.618 knn 0.568  
	spa: svm 0.787 knn 0.700
	cat: svm 0.826 knn 0.715

The result for SVM is always better than KNN for all 3 languages. SVM trained the model and maximize the margin, while KNN just determines the label by k neighbors. So because SVM is supported by learning theory, so it usually has better results than KNN.

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Part4:
a)
I removed stopwords, and do stemming with default window size 10. The result shown below indicates that removing stopwords helps English a little bit, but did not help Spanish. And I did stemming after removing stopwords, and found that in this case, stemming helps Spanish very much, but has no effect for English. And also I tried stemming without removing stop words, And found that stemming did not help for English but helps for Spanish. So I would conclude that for window size 10, removing stopwords helps English, but not for Spanish. And stemming helps Spanish but not for English.
But for smaller window size 3, the effect is different. I found that for English, stemming is much more helpful than remiving stop words. 
Removing stopwords could help eliminating some irrelevant features and improve the accuracy for classfier. And it is effective when window size is very large, because the feature vector would be very large in that case, and removing stopwords could significantly help reducing the size of feature vector. But when the window size is small, for example 3, removing stopwords cannot help too much, because in this case the stopwords are the main indicator for the sense of the word. For example, the word followed by stopword "to" is more likely to be a verb, and a word follows "a" is more likely to be a noun. So in this case, removing stopwords will hurts the performance of the classifier. 

+stopwords: 
	window = 10
		eng: svm 0.626 knn 0.567
		spa: svm 0.786 knn 0.692

	+stemming: 
		window = 3
			eng: svm 0.617 knn 0.574
			spa: svm 0.799 knn 0.725
		window = 10
			eng: svm 0.626 knn 0.570
			spa: svm 0.804 knn 0.706


+stemming: 
	window = 3:
		eng: svm 0.648 knn 0.579	
		spa: svm 0.789 knn 0.747
	window = 10:
		eng: svm 0.619 knn 0.570
		spa: svm 0.794 knn 0.711
	

b)
Also I tried adding synsets words to the feature for English. And I found that it does not help, and moreover reduced the accuracy of the result. So it indicates that although synsets give more semantic information about the context of the ambiguous word, it also introduces much more irrelevant words into the vector. So it did not help the result.

+stemming:
	+synonyms: 
		window = 10
			eng: svm 0.608 knn 0.558

c)
I computed the relevance score for each word and filter out those irrelevant words. I tried the method several times with different settings. I tried with different window size. And also pick up different number of words (n) for each sense. The result shows that for a fixed window size, increasing n will get better results. And when n is large enough, nothing is filtered. The result will be the same with part a) above. That means filtering out words with low relevance score does not help the result. 

+stemming
	+ranking(top n)
		window = 10
			n = 25
				eng: svm 0.577 knn 0.546
				spa: svm 0.758 knn 0.699
				cat: svm 0.789 knn 0.715
			n = 50
				eng: svm 0.585 knn 0.544
				spa: svm 0.776 knn 0.697
				cat: svm 0.789 knn 0.721
			n = 100
				eng: svm 0.617 knn 0.549
				spa: svm 0.770 knn 0.701
				cat: svm 0.801 knn 0.709
			n = 200
				eng: svm 0.611 knn 0.553
				spa: svm 0.786 knn 0.702
				cat: svm 0.829 knn 0.699
		window = 25
			n = 25
				eng: svm 0.574 knn 0.553
				spa: svm 0.764 knn 0.712
				cat: svm 0.798 knn 0.724
			n = 50
				eng: svm 0.577 knn 0.549
				spa: svm 0.772 knn 0.700
				cat: svm 0.793 knn 0.708
			n = 100
				eng: svm 0.593 knn 0.550
				spa: svm 0.779 knn 0.695
				cat: svm 0.801 knn 0.709
			n = 200
				eng: svm 0.608 knn 0.553
				spa: svm 0.784 knn 0.698
				cat: svm 0.790 knn 0.693


d)
From the above result and analysis, I found that removing words with low relevance is not helpful. And also the result is better when window size becomes smaller. So I decide to use small window size to train the classifier. And also consider that stopwords are good indicator for small window size, I did not remove stopwords. Small window size avoid the misdirection by irrelevant words, but it also lacks of some information about the ambiguous word. So for this end, I added the position information for each word in the window size to indicate whether the word is in the left of the ambiguous word, and also indicate how far the word is from the ambiguous word. The result is shown below. We could find that when window size is 3 the result is better than above experiments. 
The position could be a very important information for the ambiguous word in some cases. For example, the ambiguous word follows "a" is very likely to be a noun, while the word followed by "a" is less likely to be a noun and much more likely to be a verb. And the POS could help disambiguate the the word. So if we do not use position information, we are not able to distinguish the above two cases, which lead to very different results.

+stemming
	+position
		window = 3
			**eng: svm 0.669 knn 0.610**
			**spa: svm 0.812 knn 0.753**
			**cat: svm 0.823 knn 0.756**
		window = 5
			eng: svm 0.642 knn 0.609
			spa: svm 0.803 knn 0.739
			cat: svm 0.804 knn 0.721
		window = 10
			eng: svm 0.620 knn 0.590
			spa: svm 0.786 knn 0.703
			cat: svm 0.793 knn 0.697



Part5:
The method of best performance is the one described in part4d), adding position information with window size 3. 