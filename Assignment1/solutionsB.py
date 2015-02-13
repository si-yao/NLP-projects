import sys
import nltk
import math
import re
#this function takes the words from the training data and returns a python list of all of the words that occur more than 5 times
#wbrown is a python list where every element is a python list of the words of a particular sentence
def calc_known(wbrown):
    knownwords = set()
    wordCountMap = {}
    for sentWords in wbrown:
        for word in sentWords:
            wordCountMap[word] = wordCountMap.get(word, 0) + 1
    for w in wordCountMap:
        if(wordCountMap[w] > 5):
            knownwords.add(w)
    del wordCountMap
    return knownwords

#this function takes a set of sentences and a set of words that should not be marked '_RARE_'
#brown is a python list where every element is a python list of the words of a particular sentence
#and outputs a version of the set of sentences with rare words marked '_RARE_'
def replace_rare(brown, knownwords):
    rare = []
    for sentWords in brown:
        sentence = []
        for word in sentWords:
            if(word in knownwords):
                sentence.append(word)
            else:
                sentence.append("_RARE_")
        rare.append(sentence)
    return rare

#this function takes the ouput from replace_rare and outputs it
def q3_output(rare):
    outfile = open("B3.txt", 'w')

    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()

#this function takes tags from the training data and calculates trigram probabilities
#tbrown (the list of tags) should be a python list where every element is a python list of the tags of a particular sentence
#it returns a python dictionary where the keys are tuples that represent the trigram, and the values are the log probability of that trigram
def calc_trigrams(tbrown):
    qvalues = {}
    biCountMap = {}
    sentCount = len(tbrown)
    for sentTags in tbrown:
        for i, tag in enumerate(sentTags):
            if(i >= 1):
                biTuple = tuple([sentTags[i-1], sentTags[i]])
                biCountMap[biTuple] = biCountMap.get(biTuple, 0) + 1
            if(i >= 2):
                triTuple = tuple([sentTags[i-2], sentTags[i-1], sentTags[i]])
                qvalues[triTuple] = qvalues.get(triTuple, 0) + 1

    for tri in qvalues:
        if(tri[0]=="*" and tri[1]=="*"):
            base = sentCount
        else:
            base = biCountMap[tuple([tri[0],tri[1]])]
        qvalues[tri] = math.log(qvalues[tri],2) - math.log(base,2)

    del biCountMap
    return qvalues

#this function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(qvalues):
    #output
    outfile = open("B2.txt", "w")
    for trigram in qvalues:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(qvalues[trigram])])
        outfile.write(output + '\n')
    outfile.close()

#this function calculates emission probabilities and creates a list (ok for list) of possible tags
#the first return value is a python dictionary where each key is a tuple in which the first element is a word
#and the second is a tag and the value is the log probability of that word/tag pair
#and the second return value is a list of possible tags for this data set
#wbrown is a python list where each element is a python list of the words of a particular sentence
#tbrown is a python list where each element is a python list of the tags of a particular sentence
def calc_emission(wbrown, tbrown):
    evalues = {}
    taglist = []
    tagCountMap = {}
    for i, sentWords in enumerate(wbrown):
        for j, word in enumerate(sentWords):
            tag = tbrown[i][j]
            wt_tuple = tuple([word, tag])
            evalues[wt_tuple] = evalues.get(wt_tuple, 0) + 1
            tagCountMap[tag] = tagCountMap.get(tag, 0) + 1
    for wt in evalues:
        tag = wt[1]
        evalues[wt] = math.log(evalues[wt],2) - math.log(tagCountMap[tag],2)
    for tag in tagCountMap:
        taglist.append(tag)

    return evalues, taglist

#this function takes the output from calc_emissions() and outputs it
def q4_output(evalues):
    #output
    outfile = open("B4.txt", "w")
    for item in evalues:
        output = " ".join([item[0], item[1], str(evalues[item])])
        outfile.write(output + '\n')
    outfile.close()


#this function takes data to tag (brown), possible tags (taglist), a list of known words (knownwords),
#trigram probabilities (qvalues) and emission probabilities (evalues) and outputs a list where every element is a string of a
#sentence tagged in the WORD/TAG format
#brown is a list where every element is a list of words
#taglist is from the return of calc_emissions()
#knownwords is from the the return of calc_knownwords()
#qvalues is from the return of calc_trigrams
#evalues is from the return of calc_emissions()
#tagged is a list of tagged sentences in the format "WORD/TAG". Each sentence is a string with a terminal newline, not a list of tokens.
def viterbi(brown, taglist, knownwords, qvalues, evalues):
    tagged = []
    for sentWords in brown:
        taggedWords = viterbilet(sentWords, taglist, qvalues, evalues)
        print "taggedWords:"
        print taggedWords
        tagged.append(taggedWords)
    return tagged


def viterbilet(sentWords, taglist, qvalues, evalues):
    taggedWords = []
    m = len(taglist) # number of tags
    n = len(sentWords) # number of words
    #3D array with dimension m*n*m
    #A is the DP array storing the best trigram prob.
    #A[j][i][k] represents:
    #for the i-th word, if the tag is tag[j], and previous word is tag[k], 
    #then the best prob now for [anyBestTags],word[i-1]/tag[k],word[i]/tag[j] is A[j][i][k]
    #and D[j][i][k] indicates the best tag for word[i-2], the tag 2 behind i-th word
    A = m*[n*[m*[0]]] 
    D = m*[n*[m*[0]]]
    for i, word in enumerate(sentWords):# each word
        if(i < 2):
            for j in range(0,m):
                for k in range(0,m):
                    A[j][i][k] = 0
            continue

        for j in range(0,m):# index of current tag for this word
            tag = taglist[j]# current tag
            for k in range(0,m):# index of tag 1 behind
                maxi = -100000000000000
                maxtag = 0
                for kk in range(0,m):# index of tag 2 behind
                    tri_tuple = tuple([taglist[kk], taglist[k], taglist[j]])
                    if(i==2):
                        tri_tuple = tuple("*", "*", taglist[j])
                    elif(i==3):
                        tri_tuple = tuple("*", taglist[k], taglist[j])

                    cur = A[k][i-1][kk] + qvalues.get(tri_tuple, -1000) + evalues.get(tuple([word, tag]), -1000)
                    if(cur > maxi):
                        maxi = cur
                        maxtag = kk
                A[j][i][k] = maxi
                D[j][i][k] = maxtag
    curmax = -100000000000000
    curmaxI = 0
    prevI = 0
    # for the last word, find the best 1 behind tag, and best 2 behind tag
    for j in range(0,m):
        for k in range(0,m):
            if(A[j][n-1][k] > curmax):
                curmaxI = j
                prevI = k
    #print A
    revTagList = [taglist[curmaxI], taglist[prevI]]
    #for each loop, using curmaxI and prevI, we could find the previous 1 best tag.
    for i in range(n-1,3,-1):
        tmp = D[curmaxI][i][prevI]
        #print "curmaxI:", curmaxI, " i:", i, " prevI:", prevI
        #print "D = ", tmp
        curmaxI = prevI
        prevI = tmp
        revTagList.append(taglist[tmp])

    #at beginning, there are 2 *
    revTagList.append("*")
    revTagList.append("*")
    revTagList.reverse()

    #form the tagwords
    #print revTagList
    for i, word in enumerate(sentWords):
        taggedWords.append(word+"/"+revTagList[i])
    del A
    del D
    return taggedWords



#this function takes the output of viterbi() and outputs it
def q5_output(tagged):
    outfile = open('B5.txt', 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

#this function uses nltk to create the taggers described in question 6
#brown is the data to be tagged
#tagged is a list of tagged sentences the WORD/TAG format. Each sentence is a string with a terminal newline rather than a list of tokens.
def nltk_tagger(brown):
    tagged = []
    return tagged

def q6_output(tagged):
    outfile = open('B6.txt', 'w')
    for sentence in tagged:
        outfile.write(output)
    outfile.close()

#a function that returns two lists, one of the brown data (words only) and another of the brown data (tags only)
def split_wordtags(brown_train):
    # those 2 are list of list. each ele in it is a list containing words (or tags) of a sentence.
    wbrown = []
    tbrown = []
    for sentence in brown_train:
        wordsWithTag = sentence.split(" ")
        wordsWithTag = ["*/*", "*/*"] + wordsWithTag + ["STOP/STOP"]
        sentWords = []
        sentTags = []
        #print wordsWithTag
        for wordTag in wordsWithTag:
            wordTagSplit = re.split("/(?=[^/]+\Z)", wordTag)
            if(len(wordTagSplit)<2):
                continue
            sentWords.append(wordTagSplit[0])
            sentTags.append(wordTagSplit[1])
        wbrown.append(sentWords)
        tbrown.append(sentTags)

    return wbrown, tbrown

#Format sentences, and tag rare words as _RARE_.
#Returns list of list. each ele in the return list is a list of words in one line.
def formatDev(brown_dev, knownwords):
    brown_rst = []
    for sent in brown_dev:
        sentWords = nltk.word_tokenize(sent)
        sentWords = ["*", "*"] + sentWords + ["STOP"]
        for i, word in enumerate(sentWords):
            if(not(word in knownwords)):
                sentWords[i] = "_RARE_"
        brown_rst.append(sentWords)
    return brown_rst


def main():
    #open Brown training data
    infile = open("Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    #split words and tags, and add start and stop symbols (question 1)
    wbrown, tbrown = split_wordtags(brown_train)

    #calculate trigram probabilities (question 2)
    qvalues = calc_trigrams(tbrown)

    #question 2 output
    q2_output(qvalues)
    
    
    #calculate SET of words with count > 5 (question 3)
    knownwords = calc_known(wbrown)

    #get a version of wbrown with rare words replace with '_RARE_' (question 3)
    wbrown_rare = replace_rare(wbrown, knownwords)

    #question 3 output
    q3_output(wbrown_rare)
    
    #calculate emission probabilities (question 4)
    evalues, taglist = calc_emission(wbrown_rare, tbrown)

    #question 4 output
    q4_output(evalues)

    #delete unneceessary data
    del brown_train
    del wbrown
    del tbrown
    del wbrown_rare
    
    #open Brown development data (question 5)
    infile = open("Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    #format Brown development data here
    brown_dev = formatDev(brown_dev, knownwords)

    #do viterbi on brown_dev (question 5)
    viterbi_tagged = viterbi(brown_dev, taglist, knownwords, qvalues, evalues)

    #question 5 output
    q5_output(viterbi_tagged)
    '''
    #do nltk tagging here
    nltk_tagged = nltk_tagger(brown_dev)

    #question 6 output
    q6_output(nltk_tagged)
    '''
if __name__ == "__main__": main()
