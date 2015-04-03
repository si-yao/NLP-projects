Part3:
window = 10
	eng: svm 0.618 knn 0.568  
	spa: svm 0.787 knn 0.700
	cat: svm 0.826 knn 0.715


Part4:
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
	
	+synonyms: 
		window = 10
			eng: svm 0.608 knn 0.558

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

+position
	+stemming
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

