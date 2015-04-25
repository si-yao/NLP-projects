import nltk
from nltk.align.ibm1 import IBMModel1
from collections import defaultdict
from nltk.align import AlignedSent
import A

class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # TODO: Computes the alignments for align_sent, using this model's parameters. Return
    #       an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
        alignment = []

        l_e = len(align_sent.words)
        l_f = len(align_sent.mots)

        for j, en_word in enumerate(align_sent.words):
            
            # Initialize the maximum probability with Null token
            max_align_prob = (self.t[en_word][None]*self.q[0][j+1][l_e][l_f], None)
            for i, fr_word in enumerate(align_sent.mots):
                # Find out the maximum probability
                max_align_prob = max(max_align_prob,
                    (self.t[en_word][fr_word]*self.q[i+1][j+1][l_e][l_f], i))

            # If the maximum probability is not Null token,
            # then append it to the alignment. 
            if max_align_prob[1] is not None:
                alignment.append((j, max_align_prob[1]))

        return AlignedSent(align_sent.words, align_sent.mots, alignment)
    
    # TODO: Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
        fr_vocab = set()
        en_vocab = set()
        for alignSent in aligned_sents:
            en_vocab.update(alignSent.words)
            fr_vocab.update(alignSent.mots)
        aligned_sents_inv = [e.invert() for e in aligned_sents]

        t_ef, align = self.initParam(aligned_sents)
        t_ef_inv, align_inv = self.initParam(aligned_sents_inv)
        for i in range(0, num_iters):
            #Train the original one
            fr_vocab.add(None)
            t_ef, align = self.EMIteration(t_ef, align, en_vocab, fr_vocab, aligned_sents)
            fr_vocab.remove(None)
            #Train the inverse one
            en_vocab.add(None)
            t_ef_inv, align_inv = self.EMIteration(t_ef_inv, align_inv, fr_vocab, en_vocab, aligned_sents_inv)
            en_vocab.remove(None)
            t_ef_new, align_new = self.agree(t_ef, align, t_ef_inv, align_inv)
            t_ef_inv_new, align_inv_new = self.agree(t_ef_inv, align_inv, t_ef, align)
            t_ef, align = t_ef_new, align_new
            t_ef_inv, align_inv = t_ef_inv_new, align_inv_new

        return t_ef, align


    def agree(self, t_ef, align, t_ef_inv, align_inv):
        #t_ef_new = defaultdict(lambda: defaultdict(lambda: 0.0))
        #t_ef_inv_new = defaultdict(lambda: defaultdict(lambda: 0.0))
        #total_f = defaultdict(float)
        #for e in t_ef:
        #    for f in t_ef[e]:
        #        comp = t_ef_inv[f][e]
        #        t_ef_new[e][f] = (t_ef[e][f]+comp)/2.0
        #        total_f[f] += t_ef_new[e][f]
        #for e in t_ef_new:
        #    for f in t_ef_new[e]:
        #        t_ef_new[e][f] = t_ef_new[e][f]/total_f[f]


        align_new = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
        total_align = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
        for f_i in align:
            for e_i in align[f_i]:
                for l_e in align[f_i][e_i]:
                    for l_f in align[f_i][e_i][l_e]:
                        comp = align_inv[e_i][f_i][l_f][l_e]
                        align_new[f_i][e_i][l_e][l_f] = (align[f_i][e_i][l_e][l_f]+comp)/2.0
                        total_align[e_i][l_e][l_f] += align_new[f_i][e_i][l_e][l_f]
        for f_i in align:
            for e_i in align[f_i]:
                for l_e in align[f_i][e_i]:
                    for l_f in align[f_i][e_i][l_e]:
                        align_new[f_i][e_i][l_e][l_f] /= total_align[e_i][l_e][l_f]
        return t_ef, align_new


    def initParam(self, align_sents):
        #ibm1 = IBMModel1(align_sents, 5)
        #t_ef = ibm1.probabilities

        align = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
        # Initialize the distribution of alignment probability,
        # a(i|j,l_e, l_f) = 1/(l_f + 1)
        for alignSent in align_sents:
            en_set = alignSent.words
            fr_set = [None] + alignSent.mots
            l_f = len(fr_set) - 1
            l_e = len(en_set)
            initial_value = 1.0 / (l_f + 1)
            for i in range(0, l_f+1):
                for j in range(1, l_e+1):
                    align[i][j][l_e][l_f] = initial_value

        init_prob = 1.0 / l_e
        # Create the translation model with initial probability
        t_ef = defaultdict(lambda: defaultdict(lambda: init_prob))
        return t_ef, align

    def EMIteration(self, t_ef, align, en_vocab, fr_vocab, align_sents):
        #print("A iteration")
        count_ef = defaultdict(lambda: defaultdict(float))
        total_f = defaultdict(float)

        count_align = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
        total_align = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

        total_e = defaultdict(float)

        for alignSent in align_sents:
            en_set = alignSent.words
            fr_set = [None] + alignSent.mots
            l_f = len(fr_set) - 1
            l_e = len(en_set)

            # compute normalization
            for j in range(1, l_e+1):
                en_word = en_set[j-1]
                total_e[en_word] = 0
                for i in range(0, l_f+1):
                    total_e[en_word] += t_ef[en_word][fr_set[i]] * align[i][j][l_e][l_f]
                    #print(align[i][j][l_e][l_f])

            # collect counts
            for j in range(1, l_e+1):
                en_word = en_set[j-1]
                for i in range(0, l_f+1):
                    fr_word = fr_set[i]
                    c = t_ef[en_word][fr_word] * align[i][j][l_e][l_f] / total_e[en_word]
                    count_ef[en_word][fr_word] += c
                    total_f[fr_word] += c
                    count_align[i][j][l_e][l_f] += c
                    total_align[j][l_e][l_f] += c

        # estimate probabilities
        t_ef = defaultdict(lambda: defaultdict(lambda: 0.0))
        align = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))

        # Smoothing the counts for alignments
        for alignSent in align_sents:
            en_set = alignSent.words
            fr_set = [None] + alignSent.mots
            l_f = len(fr_set) - 1
            l_e = len(en_set)

            laplace = 1.0
            for i in range(0, l_f+1):
                for j in range(1, l_e+1):
                    value = count_align[i][j][l_e][l_f]
                    if 0 < value < laplace:
                        laplace = value

            laplace *= 0.5 
            for i in range(0, l_f+1):
                for j in range(1, l_e+1):
                    count_align[i][j][l_e][l_f] += laplace

            initial_value = laplace * l_e
            for j in range(1, l_e+1):
                total_align[j][l_e][l_f] += initial_value
        
        # Estimate the new lexical translation probabilities
        for f in fr_vocab:
            for e in en_vocab:
                t_ef[e][f] = count_ef[e][f] / total_f[f]

        # Estimate the new alignment probabilities
        for alignSent in align_sents:
            en_set = alignSent.words
            fr_set = [None] + alignSent.mots
            l_f = len(fr_set) - 1
            l_e = len(en_set)
            for i in range(0, l_f+1):
                for j in range(1, l_e+1):
                    align[i][j][l_e][l_f] = count_align[i][j][l_e][l_f] / total_align[j][l_e][l_f]
        return t_ef, align

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 20)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))