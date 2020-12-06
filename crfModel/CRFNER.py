#from itertools import chain

#import nltk
#import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV
import scipy
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
from pprint import pprint
import random
import pickle
import matplotlib.pyplot as plt

from FeatureExtraction import sent2labels,sent2features
from PhraseEval import phrasesFromTestSenJustExtraction,phrase_extraction_report
from DataExtraction import convertCONLLFormJustExtractionSemEval

def main():
    # trainingCorpus = 'larger'
    trainingCorpus = 'original'
    trainFile = "medicalData/convertedBIO/" + trainingCorpus + "/combinedTrain.txt"
    testFile  = "medicalData/convertedBIO/" + trainingCorpus + "/combinedTest.txt"
    
    train_sents = convertCONLLFormJustExtractionSemEval(trainFile)
    test_sents = convertCONLLFormJustExtractionSemEval(testFile)
    
    # train_sents = convertCONLLFormJustExtractionSemEval("medicalData/convertedBIO/combinedTrain.txt")
    # test_sents = convertCONLLFormJustExtractionSemEval("medicalData/convertedBIO/combinedTest.txt")
    
    # pprint(train_sents[0])
    # print('\n')
    # pprint(test_sents[0])
    # print('\n')
        
    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]

    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    crf = sklearn_crfsuite.CRF(\
    algorithm='lbfgs',\
    # c1=0.1,\
    # c2=0.1,\
    c1=0.12,\
    c2=0.23,\
    max_iterations=100,\
    all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    
    if trainingCorpus == 'larger':
        labels = list(crf.classes_)
        labels.remove('O')
        labels.remove('1')
        labels.remove('3')
        labels.remove('8')
        labels.remove('9')
    elif trainingCorpus == 'original':   
        labels = list(crf.classes_)
        labels.remove('O')
    # print(labels)
    print('\n')
    pickle.dump(crf,open("medicalData/linear-chain-crf.model.pickle","wb"), protocol = 0, fix_imports = True)
    y_pred = crf.predict(X_test)
 #%%    
    # Use this if you need to do grid search on training data for parameter optimization.
    # %%
    # define fixed parameters and parameters to search
    # crf = sklearn_crfsuite.CRF(
    #     algorithm='lbfgs',
    #     max_iterations=100,
    #     all_possible_transitions=True
    # )
    # params_space = {
    #     'c1': scipy.stats.expon(scale=0.5),
    #     'c2': scipy.stats.expon(scale=0.05),
    # }
    
    # # use the same metric for evaluation
    # f1_scorer = make_scorer(metrics.flat_f1_score,
    #                         average='weighted', labels=labels)
    
    # # search
    # rs = RandomizedSearchCV(crf, params_space,
    #                         cv=3,
    #                         verbose=1,
    #                         n_jobs=-1,
    #                         n_iter=50,
    #                         return_train_score=True,
    #                         scoring=f1_scorer)
    # rs.fit(X_train, y_train)
    # #%%
    # # crf = rs.best_estimator_
    # print('best params:', rs.best_params_)
    # print('best CV score:', rs.best_score_)
    # print('model size: {:0.2f}M'.format(rs.best_estimator_.size_ / 1000000))
    
    # #%%
    # # _x = [s.parameters['c1'] for s in rs.cv_results_]
    # # _y = [s.parameters['c2'] for s in rs.cv_results_]
    # # _c = [s.mean_validation_score for s in rs.cv_results_]
    
    
    # _x = [s['c1'] for s in rs.cv_results_['params']]
    # _y = [s['c2'] for s in rs.cv_results_['params']]
    # _c = [s for s in rs.cv_results_['mean_train_score']]
    
        
    # fig = plt.figure()
    # fig.set_size_inches(12, 12)
    # ax = plt.gca()
    # ax.set_yscale('log')
    # ax.set_xscale('log')
    # ax.set_xlabel('C1')
    # ax.set_ylabel('C2')
    # ax.set_title("Randomized Hyperparameter Search CV Results (min={:0.3}, max={:0.3})".format(min(_c), max(_c)))

    # ax.scatter(_x, _y, c=_c, s=60, alpha=0.9, edgecolors=[0,0,0])
    

    # print("Dark blue => {:0.4}, dark red => {:0.4}".format(min(_c), max(_c)))
#%%
    sorted_labels = sorted(labels,key=lambda name: (name[1:], name[0]))
    print('\nTest Results (Training Corpus: ' + trainingCorpus + ')')
    print(metrics.flat_classification_report(y_test, y_pred, labels=sorted_labels, digits=3))
    
    print('\nTrain Results (Training Corpus: ' + trainingCorpus + ')')
    y_pred = crf.predict(X_train)
    print(metrics.flat_classification_report(y_train, y_pred, labels=sorted_labels, digits=3))
    
if __name__ == "__main__":
    main()