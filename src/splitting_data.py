import csv
import source_reader as src

def split_data(data):
    #print len(data)
    print "splitting data"
    nob = src.num_of_batch()

    train_index = int(len(data)/100)
    #batch_index = int(train_index/nob)

    train_set = data[:train_index]
    write_batch(train_set,"training")

    test_set = data[train_index:len(data)]
    nos = len(test_set)/nob #number of samples per batch
    st = 0
    en = nos

    for i in range(nob):
        if i != nob-1:
            temp_batch = test_set[st:en]
            st = st + nos
            en = en + nos
        else:
            temp_batch = test_set[st:len(data)]

        write_batch(temp_batch,i)

def write_batch(data,name):

    path = src.batch_feat(name)

    out_file = open(path, "w")
    csv_writer = csv.writer(out_file, delimiter='\t')
    for line in data:
        csv_writer.writerow(line)
    out_file.close()
