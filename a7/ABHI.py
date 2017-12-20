#!/usr/bin/env python
import argparse  # optparse is deprecated
from itertools import islice  # slicing for iterators


def word_matches(h, ref):

    sum=0
    for word in h:
        if word in ref:
            sum+=1
            ref.remove(word)
    return sum


def deep_analysis(h, ref):
    
    def gen4(list):
        res = []
        if len(list) < 4:
            return list
        for i in range(len(list) - 3):
            res.append(list[i] + " " + list[i + 1] + " " + list[i + 2]+ " " + list[i + 3])
            # print i
        return res
           

    f_h = gen4(h)
    f_ref = gen4(ref)
    f_ref_set = set(f_ref)

    f_Val= word_matches(f_h, f_ref_set)
    
    return f_Val#, triVal])/float(2)

###############


def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
                        help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
                        help='Number of hypothesis pairs to evaluate')
    # note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
    opts = parser.parse_args()

    # we create a generator and avoid loading all sentences into a list
    def sentences():
        with open(opts.input) as f:
            for pair in f:
                yield [sentence.strip() for sentence in pair.split(' ||| ')]

    def create4grams(sample_list):
            res=[]
            if len(sample_list)==1 or len(sample_list)==2 or len(sample_list)==3:
                return sample_list
            for i in range(len(sample_list)-3):
                
                res.append(sample_list[i]+" "+sample_list[i+1] + " "+sample_list[i+2] + " "+sample_list[i+3])
                    #print i
            return res 

    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        # <-------------------Unigram Matches and Chunks----------------------------------->
        h1_match = deep_analysis(h1 , ref)
        h2_match = deep_analysis(h2 , ref)

        # <-------------------Precision and Recall----------------------------------->
        if len(h1) == 0:
            h1_precision = 0.0
        else:
            h1_precision = float(h1_match) / float(len(h1))

        if len(h2) == 0:
            h2_precision = 0.0
        else:
            h2_precision = float(h2_match) / float(len(h2))

        if len(ref) == 0:
            h1_recall = 0.0
            h2_recall = 0.0
        else:
            h1_recall = float(h1_match) / float(len(ref))
            h2_recall = float(h2_match) / float(len(ref))


        # <-------------------Meteor Calculation----------------------------------->
        alpha = 0.9

        if h1_precision == 0.0 or h1_recall == 0.0:
            h1_meteor = 0.0
        else:
            h1_meteor = float(h1_precision * h1_recall) / float((alpha * h1_precision) + (1 - alpha) * (h1_recall))

        if h2_precision == 0.0 or h2_recall == 0.0:
            h2_meteor = 0.0
        else:
            h2_meteor = float(h2_precision * h2_recall) / float((alpha * h2_precision) + (1 - alpha) * (h2_recall))

        # <-------------------Print Results----------------------------------->

        print(1 if h1_meteor > h2_meteor else  # \begin{cases}
              (0 if h1_meteor == h2_meteor
               else -1))  # \end{cases}


# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
