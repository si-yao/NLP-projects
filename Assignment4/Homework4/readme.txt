PartA
3)
Average AER over the first 50 sentences for IBM1 is 0.665.
Average AER over the first 50 sentences for IBM2 is 0.650.

-------------------------------------------------------------------
#For the following sentence pair, IBM1 has better performance:

Wie Sie sicher aus der Presse und dem Fernsehen wissen , gab es in Sri Lanka mehrere Bombenexplosionen mit zahlreichen Toten .
You will be aware from the press and television that there have been a number of bomb explosions and killings in Sri Lanka .

Gold Standard Alignment: (AER 0)
0-0 1-0 2-1 2-2 3-4 4-5 5-6 6-7 7-8 8-8 9-3 10-9 11-10 11-11 11-12 12-10 13-20 14-21 15-22 16-14 16-15 17-16 17-17 17-18 17-19 19-13 21-23
Model1 Alignment: (AER 0.791666666667)
0-19 1-0 2-19 3-4 4-15 5-19 6-18 7-22 8-19 9-19 10-2 11-22 12-22 13-20 14-22 15-22 16-19 17-19 18-19 19-19 20-19
Model2 Alignment: (AER 0.833333333333)
0-6 1-0 2-16 3-4 4-4 5-17 6-18 7-22 8-19 9-8 10-2 11-21 12-22 13-20 14-19 15-22 16-19 17-8 18-17 19-19 20-8

Comments: 
Most time, IBM2 is better than IBM1. For this case, IBM1 is better than IBM2. I suspect that it is because the 2 methods both give a bad result, with AER higher than 0.75. So although IBM1 is better than IBM2, both of them do not give a good result. 

-------------------------------------------------------------------
#For the following sentence pair, IBM2 has better performance:

Ich bitte Sie , sich zu einer Schweigeminute zu erheben .
Please rise , then , for this minute ' s silence .

Gold Standard Alignment: (AER 0)
0-0 1-0 2-0 3-4 4-1 5-5 6-6 7-7 7-8 7-9 7-10 8-10 9-10 10-11
Model1 Alignment: (AER 0.75)
0-1 1-1 2-1 3-4 4-10 5-10 6-10 7-10 8-10 9-1
Model2 Alignment: (AER 0.666666666667)
0-0 1-1 2-0 3-2 4-10 5-10 6-10 7-7 8-10 9-0

Comments:
Because IBM2 takes position distortion into consideration, so the IBM2 gives better performance.



4)
========================================
                  IBM1
-----+------+------+------+------+------
Iter |  10  |  20  |  30  |  40  |  50
-----+------+------+------+------+------
AER  |0.665 |0.661 |0.660 |0.657*|0.658
========================================
                  IBM2
-----+------+------+------+------+------
Iter |  10  |  20  |  30  |  40  |  50  
-----+------+------+------+------+------
AER  |0.650 |0.648*|0.649 |0.650 |0.654
========================================

The relation between number of iteration with AER is shown as above.
The best number of iteration of IBM1 is 40, the lower bound of AER is around 0.657.
The best number of iteration of IBM2 is 20, the lower bound of AER is around 0.648.



PartB
4)
Average AER over the first 50 sentences for BerkeleyAligner model is 0.574


5)
For following sentence pair, the Berkeley Aligner performs better than the IBM models:

Ich bitte Sie , sich zu einer Schweigeminute zu erheben .
Please rise , then , for this minute ' s silence .

Gold Standard Alignment: (AER 0)
0-0 1-0 2-0 3-4 4-1 5-5 6-6 7-7 7-8 7-9 7-10 8-10 9-10 10-11
Model1 Alignment: (AER 0.75)
0-1 1-1 2-1 3-4 4-10 5-10 6-10 7-10 8-10 9-1
Model2 Alignment: (AER 0.666666666667)
0-0 1-1 2-0 3-2 4-10 5-10 6-10 7-7 8-10 9-0
BerkeleyAligner Alignment: (AER 0.6)
0-0 1-1 2-0 3-2 4-7 5-10 6-10 7-7 8-10 9-1 10-11

Comments:
Because BerkeleyAligner considers 2 translators, one from source language to target language and one from target language to source language, it usually has better performance than IBM models. For this case, BerkeleyAligner predicts more alignments than IBM models. But for all 3 models, they are not able to align 1 word to multiple words in target language.


