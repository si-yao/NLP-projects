import nltk
import codecs
from nltk.align import AlignedSent
from nltk.align import Alignment
from nltk.align.ibm1 import IBMModel1
from nltk.align.ibm2 import IBMModel2
# TODO: Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
    return IBMModel1(aligned_sents, 10);

# TODO: Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
    return IBMModel2(aligned_sents, 10);

# TODO: Compute the average AER for the first n sentences
#       in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
    count = 0;
    for i in range(0,n):
        rst = model.align(aligned_sents[i]);
        count += rst.alignment_error_rate(aligned_sents[i]);
    return 1.0*count/n;


def compare(aligned_sents, model1, model2):
    for i in range(0,10):
        rst1 = model1.align(aligned_sents[i]);
        rst2 = model2.align(aligned_sents[i]);
        aer1 = rst1.alignment_error_rate(aligned_sents[i]);
        aer2 = rst2.alignment_error_rate(aligned_sents[i]);
        if(aer1<aer2):
            print("Model1 is BETTER HERE:");
        elif(aer1>aer2):
            print("Model2 is BETTER HERE:");

        print("Gold:");
        print(aligned_sents[i].alignment);
        print("Model1:"+ str(aer1));
        print(rst1);
        print("Model2:"+ str(aer2));
        print(rst2);


# TODO: Computes the alignments for the first 20 sentences in
#       aligned_sents and saves the sentences and their alignments
#       to file_name. Use the format specified in the assignment.
def save_model_output(aligned_sents, model, file_name):
    fout = codecs.open(file_name, encoding = 'utf-8', mode = 'w')
    for i in range(0,20):
        rst = model.align(aligned_sents[i]);
        fout.write(" ".join(rst.words));
        fout.write("\n");
        fout.write(" ".join(rst.mots));
        fout.write("\n");
        fout.write(rst.alignment);
        fout.write("\n\n");
    fout.close();

def main(aligned_sents):
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
    
    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    compare(aligned_sents, ibm1, ibm2);
    