readme

---------------
Assumptions:

There is a 'Data' sub-directory in project directory. This holds a sub-directory
called 'lexicon'. Lexicon directory holds a same or less files as provided
to assist in feature engineering.

same training file name and directory path as in provided set

---------------------------
To run logistic regression:

python main.py --eval <TESTFILE>

---------------------------

To run CRF:
Please use the tagger.py that i uploaded instead of default one from you.
I modified Perceptron parameters in it. 
It took ~40 min on modified parameters, and ~20 min without using modified parameters

python main.py --tagger crf --eval <TESTFILE>