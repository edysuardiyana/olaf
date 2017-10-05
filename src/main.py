import csv
import eves
import source_reader as src
from collections import namedtuple
import random
import splitting_data as sd
import olaf_main as olaf
import plot_experiment as ple


ARRAY_TUPLED = namedtuple('ARRAY_TUPLED', 'AXC AYC AZC GXC GYC GZC AVMC GVMC'
                                 ' AXT AYT AZT GXT GYT GZT AVMT GVMT ANNOT')

def main():
    #read listname
    listname_path = src.listname_path()
    listname = read_list_name(listname_path)
    freq_rate = src.freq_rate()
    noe = src.num_of_exp()

    #extract features
    #print extract features from subjects
    extract_features(listname,freq_rate)

    #loop for each type of classifier: 0. Logreg, 1. SGD without update, 2. SGD with update
    tot_plot = [] # to collect data for plotting
    for cl in range(3):

        for i in range(noe):
            print "Experiment number: "+str(i)

            #load all data
            tot_data,len_data = read_features(listname)

            #split the batch
            sd.split_data(tot_data)

            #run olaf training_set
            runtime_pool, num_of_false = olaf.olaf_main(i,cl)

            path_false = src.falses_num(str(cl)+"/falses_"+str(i))
            write(num_of_false, path_false)

            if cl == 2:
                path = src.runtime("runtime_"+str(i))
                write(runtime_pool,path)



        #plot & print data
        if cl == 0:
            print "================= Classifier: Logistic Regression ================="
        elif cl == 1:
            print "================= Classifier: SGD without updating ================="
        else:
            print "================= Classfier: SGD with update ================="

        temp_plot = ple.main_plot(noe,cl)
        tot_plot.append(temp_plot)

    write_plot(tot_plot)
    print "Done Capt!"

def write_plot(data):
    fin_array = []
    path = src.plotting("result")
    header = ["Logistic_Regression","SGD", "Updated-SGD"]
    fin_array.append(header)

    for i in range(len(data[0])):
        temp_data = [data[0][i], data[1][i], data[2][i]]
        fin_array.append(temp_data)

    write(fin_array,path)

def read_features(listname):
    print "Combining features from all subjects"
    data = []
    for name in listname:
        path = src.features(name)
        with open(path) as obj:
            for line in obj:
                raw = line.split()
                temp_data = [float(i) for i in raw[:len(raw)]]
                fin_data = temp_data[:len(temp_data)-2]
                fin_data.append(temp_data[len(temp_data)-1])
                data.append(fin_data)

    print "Writing features from all subjects"
    path = src.features("Full")
    write(data,path)

    #shuffle the data
    random.shuffle(data)
    path = src.features("R_Full")
    write(data,path)

    return data,len(data)

def extract_features(listname,freq_rate):
    for name in listname:
        print "Extracting features from: " +name
        x, y, z, annot = read_seq(name)
        instance_eves,_,_  = eves.eves_window(x, y, z, annot, freq_rate, name)
        path = src.features(name)
        write(instance_eves, path)

def read_list_name(path):
    names = []
    with open(path) as obj:
        for line in obj:
            raw = line.split()
            names.append(raw[0])
    return names

def read_seq(name):
    path = src.raw_data(name)
    x = []
    y = []
    z = []
    annot = []
    with open(path) as accel:
        for line in accel:
            raw_data = line.split()
            ori_data = [float(i) for i in raw_data[:len(raw_data)]]
            tupled_data = ARRAY_TUPLED(*ori_data)
            x.append(tupled_data.AXC)
            y.append(tupled_data.AYC)
            z.append(tupled_data.AZC)
            annot.append(tupled_data.ANNOT)
    return x,y,z, annot

def write(data_seq,path):
    out_file = open(path, "w")
    csv_writer = csv.writer(out_file, delimiter='\t')
    for line in data_seq:
        csv_writer.writerow(line)
    out_file.close()


if __name__ == '__main__':
    main()
