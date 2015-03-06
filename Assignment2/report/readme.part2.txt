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

From the result we could see the badfeatures.model has poor performance for all of the languages. And also we could see that for Swedish, it has 0.125 accuracy, while for other language, it has nearly 0 accuracy. So I can conclude that this model is trained by Swedish sentences. The possible reason for the poor performance is because it did not select useful features in the training part. The model is very likely trained by the sample code provided in featureextractor.py. The feature selection in featureextractor.py has 2 main problems. 1) lack of important features. 2) should set NULL value for words that do not have certain features. NULL is also a information, so if we just add nothing when a word does not have those feature, then we actually lose some information about the configuration.

