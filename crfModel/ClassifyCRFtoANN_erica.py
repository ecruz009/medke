import pickle

from pprint import pprint

from sklearn_crfsuite import metrics

from DataExtraction import convertCONLLFormJustExtractionSemEvalPerfile
from FeatureExtraction import sent2labels,sent2features
from PhraseEval import phrasesFromTestSenJustExtractionWithIndex

import glob
    
#%%  
testFiles = glob.glob('medicalData/convertedBIO/test/*.txt')

#%% 
for fileinLoc in testFiles:
    # fileinLoc = f
    fileoutLoc = fileinLoc.split(".")[0]+".ann"
    fileoutLoc = fileoutLoc[30:]
    fileoutLoc = "medicalData/predictedANN/" + fileoutLoc
    #%%
    
    crf = pickle.load(open("medicalData/linear-chain-crf.model.pickle", "rb"))
    (test_sents,test_sents_indices) = convertCONLLFormJustExtractionSemEvalPerfile(fileinLoc)
    
    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]
    
    y_pred = crf.predict(X_test)
    
    labels = list(crf.classes_)
    # labels.remove('O')
    labels.remove('O')
    labels.remove('1')
    labels.remove('3')
    labels.remove('8')
    labels.remove('9')
    
    # print(labels)
    sorted_labels = sorted(labels,key=lambda name: (name[1:], name[0]))
    print((metrics.flat_classification_report(y_test, y_pred, labels=sorted_labels, digits=3)))
    
    test_sents_pls = []  #test sentences with predicted labels
    for index,testsent in enumerate(test_sents):
        sent=[]
        pls = y_pred[index]
        for (token,pl) in zip(testsent,pls):
            nt=(token[0],token[1],pl)
            sent.append(nt)
        test_sents_pls.append(sent)
    
    test_sents_pls_phrases=[phrasesFromTestSenJustExtractionWithIndex(x,y) for (x,y) in zip(test_sents_pls,test_sents_indices)]
    i=0
    with open(fileoutLoc,"w", encoding = 'utf8') as f:
        for sen in test_sents_pls_phrases:
            phrases=sen[-1]['phrases']
            for (p,pis,pie) in phrases:
                f.write("T{0}\tKEYPHRASE_NOTYPES {1} {2}\t{3}\n".format(str(i),pis,pie,p))
                i+=1
    print("classified file written at",fileoutLoc)


