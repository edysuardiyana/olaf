from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn import tree,svm
import csv
import source_reader as src
import random
import matplotlib.pyplot as plt
import numpy as np
import timeit
import normalization_feat as nf

def olaf_main(exp, cl):
    pool_P = [] #comment for reset
    pool_ann_P = [] #comment for reset
    pool_N = [] #comment for reset
    pool_ann_N = [] #comment for reset
    runtime_pool = []

    num_of_false = []
    print "training and testing"
    result_final = []

    nob = src.num_of_batch()

    #load testing set
    training_set, training_annot = read_data("training")

    #train initial classifier
    if cl == 0:
        clf= LogisticRegression(C = 1e9)#
        classifier = clf.fit(training_set, training_annot)
    elif cl == 1:
        clf = SGDClassifier(loss="log",penalty='l2')
        classifier = clf.fit(training_set, training_annot)
    else:
        clf = SGDClassifier(loss="log",penalty='l2', learning_rate = 'constant',eta0 = 0.001)
        #print clf
        classifier = clf.partial_fit(training_set, training_annot, classes=np.unique(training_annot))

    #start the iteration of SGD
    F_score_temp = []
    for i in range(nob):
        #pool_P = [] #comment for non-reset
        #pool_ann_P = [] #comment for non-reset
        #pool_N = [] #comment for non-reset
        #pool_ann_N = [] #comment for non-reset
        update_batch = []
        update_annot = []

        batch_data, batch_annot = read_data(i)
        result = classifier.predict(batch_data)
        result_print = adding_val_predict(result)
        #write('predict',"experiment_"+str(i),result_print)

        #Check Prec, Rec, F-score
        TP,FP,TN,FN,Prec,Rec,Fscore,index_P, index_N = metrics_calc(batch_annot,result)
        #temp_false = len(index_P) + len(index_N)

        #num_of_false.append([temp_false,0])
        #add metrics result
        temp_data = [str(i),TP,FP,TN,FN,Prec,Rec,Fscore]
        result_final.append(temp_data)

        if cl == 2:
            #print "get here"
            #classifier.partial_fit(batch_data,batch_annot)
            for line_p in index_P:
                pool_P.append(batch_data[line_p])
                pool_ann_P.append(batch_annot[line_p])

            for line_n in index_N:
                pool_N.append(batch_data[line_n])
                pool_ann_N.append(batch_annot[line_n])

            #print "getting here"
            updated_data,updated_annot = shuffling_batch(pool_P,pool_ann_P, pool_N, pool_ann_N)
            num_of_false.append([len(updated_data),0])
            #print updated_data
            if updated_data:
                start_time = timeit.default_timer()# time.clock()
                classifier.partial_fit(updated_data,updated_annot)
                end_time = timeit.default_timer()

                rt = end_time-start_time
                runtime_pool.append([rt,0])

    write('result', 'cl_'+str(cl)+'_result_'+str(exp),result_final)

    return runtime_pool,num_of_false

def shuffling_batch(pool_fp, pool_ann_fp, pool_fn, pool_ann_fn):

    tot_data = []
    data = []
    annot = []
    #fp data
    for i in range(len(pool_fp)):
        temp_data_P = [pool_fp[i],pool_ann_fp[i]]
        #print temp_data
        tot_data.append(temp_data_P)


    #fn data
    for j in range(len(pool_fn)):
        temp_data_N = [pool_fn[j],pool_ann_fn[j]]
        #print temp_data
        tot_data.append(temp_data_N)

    random.shuffle(tot_data)

    #split data into data and annot
    #print len(tot_data)
    for elem in tot_data:
        data.append(elem[0])
        annot.append(elem[1])

    return data, annot

def adding_val_predict(arr):
    fin = []
    for i in range(len(arr)):
        temp = [arr[i],0]
        fin.append(temp)

    return fin

def write(code, name, data):
    if code == 'predict':
        path = src.predict(name)
    else:
        path = src.result(name)

    out_file = open(path, "w")
    csv_writer = csv.writer(out_file, delimiter='\t')
    for line in data:
        csv_writer.writerow(line)
    out_file.close()

def read_data(name):
    path = src.batch_feat(name)
    with open(path) as obj:
        data = []
        annot = []
        for line in obj:
            raw = line.split()
            temp_data = [float(i) for i in raw[:len(raw)]]
            data.append(temp_data[:len(temp_data)-1])
            annot.append(temp_data[len(temp_data)-1])
    #print data
    #print "#################################"
    new_data = nf.norm_feat(data)
    #print new_data
    return new_data,annot #data, annot #

def metrics_calc(annot,predict):
    index_P = []
    index_N = []

    index_fault = []
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for i in range(len(annot)):
        result = accuracy_check(predict[i],annot[i])
        if result == 1:
            TP = TP+1
            #index_P.append(i)
        elif result == 2:
            FP = FP + 1
            index_N.append(i)
        elif result == 3:
            TN = TN + 1
            #index_N.append(i)
        else:
            FN = FN + 1
            index_P.append(i)

    if TP == 0 and FP == 0:
        Prec = 0
    else:
        Prec = float(TP)/(TP+FP) * 100

    if TP == 0 and FN == 0:
        Rec = 0
    else:
        Rec = float(TP)/(TP + FN) * 100

    if (2*TP)+FP+FN == 0:
        Fscore = 0
    else:
        Fscore = float((2*TP))/((2*TP)+FP+FN) * 100

    return TP,FP,TN,FN,Prec,Rec,Fscore,index_P, index_N


def accuracy_check(final_detec_flag, annot):

    result = 0
    if annot == 1 and final_detec_flag == 1:
        #true positive
        result = 1
    elif annot == 0  and final_detec_flag == 1:
        #false positive
        result = 2
    elif annot == 0 and final_detec_flag == 0:
        #true negative
        result = 3
    else: #in Fall Set and not final_detec_flag
        #false negative
        result = 4

    return result
