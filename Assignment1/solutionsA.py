import nltk
#a function that calculates unigram, bigram, and trigram probabilities
#brown is a python list of the sentences
#this function outputs three python dictionaries, where the key is a tuple expressing the ngram and the value is the log probability of that ngram
#make sure to return three separate lists: one for each ngram
def calc_probabilities(brown):
    unigram_p = {}
    bigram_p = {}
    trigram_p = {}
    for sent in brown:
        tokens = nltk.word_tokenize(sent)
        tokens = ["*"] + tokens + ["STOP"]
        for i, tok in enumerate(tokens):
            uni_tuple = tuple([tok])
            if(uni_tuple in unigram_p):
                unigram_p[uni_tuple] = unigram_p[uni_tuple]+1
            else:
                unigram_p[uni_tuple] = 1
            
            if(i >= len(tokens)-1):
                continue
            bi_tuple = tuple([tok, tokens[i+1]])
            if(bi_tuple in bigram_p):
                bigram_p[bi_tuple] = bigram_p[bi_tuple]+1
            else:
                bigram_p[bi_tuple] = 1

            if(i >= len(tokens)-2):
                continue
            tri_tuple = tuple([tok, tokens[i+1],tokens[i+2]])
            if(tri_tuple in trigram_p):
                trigram_p[tri_tuple] = trigram_p[tri_tuple]+1
            else:
                trigram_p[tri_tuple] = 1

    return unigram_p, bigram_p, trigram_p


#each ngram is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams):
    #output probabilities
    outfile = open('A1.txt', 'w')
    for unigram in unigrams:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')
    for bigram in bigrams:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')
    for trigram in trigrams:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')
    outfile.close()
    
#a function that calculates scores for every sentence
#ngram_p is the python dictionary of probabilities
#n is the size of the ngram
#data is the set of sentences to score
#this function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, data):
    scores = []
    return scores


#this function outputs the score output of score()
#scores is a python list of scores, and filename is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()


#this function scores brown data with a linearly interpolated model
#each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
#like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, brown):
    scores = []
    return scores

def main():
    #open data
    infile = open('Brown_train.txt', 'r')
    brown = infile.readlines()
    infile.close()

    #calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(brown)

    #question 1 output
    q1_output(unigrams, bigrams, trigrams)
'''
    #score sentences (question 2)
    uniscores = score(unigrams, 1, brown)
    biscores = score(bigrams, 2, brown)
    triscores = score(trigrams, 3, brown)

    #question 2 output
    score_output(uniscores, 'A2.uni.txt')
    score_output(biscores, 'A2.bi.txt')
    score_output(triscores, 'A2.tri.txt')

    #linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, brown)

    #question 3 output
    score_output(linearscores, 'A3.txt')

    #open Sample1 and Sample2 (question 5)
    infile = open('Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open('Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    #score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    #question 5 output
    score_output(sample1scores, 'Sample1_scored.txt')
    score_output(sample2scores, 'Sample2_scored.txt')
'''
if __name__ == "__main__": main()
