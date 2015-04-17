import nltk
import A

# TODO: (Optional) Improve the BerkeleyAligner.
class BetterBerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    def align(self, align_sent):

    def train(self, aligned_sents, num_iters):

def main(aligned_sents):
    ba = BetterBerkeleyAligner(aligned_sents, 20)
    if ba.t is None:
        print "Better Berkeley Aligner Not Implemented"
    else:
        avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

        print ('Better Berkeley Aligner')
        print ('---------------------------')
        print('Average AER: {0:.3f}\n'.format(avg_aer))
