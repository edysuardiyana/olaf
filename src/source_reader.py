import ConfigParser
import os
import os.path as path
import sys

def configParser(section):
    script_dir = os.path.dirname(__file__)
    real_path = os.path.join(script_dir,'path.ini')
    Config = ConfigParser.ConfigParser()
    Config.read(real_path)
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def head_path():
    head_path = path.abspath(path.join(__file__ , "../.."))
    return head_path

def listname_path():
    path = configParser("DataPath")['list_name']
    header = head_path()
    full_path = header + path
    return full_path

def raw_data(name):
    path = configParser("DataPath")['raw_data']
    header = head_path()
    full_path = header + path + name+".csv"
    return full_path

def features(name):
    path = configParser("DataPath")['features']
    header = head_path()
    full_path = header + path + name+".csv"
    return full_path

def batch_feat(num):
    path = configParser("DataPath")['batch_feat']
    header = head_path()
    full_path = header + path + str(num)+".csv"
    return full_path

def result(batch):
    path = configParser("DataPath")['result']
    header = head_path()
    full_path = header + path +str(batch)+".csv"
    return full_path

def predict(name):
    path = configParser("DataPath")['predict']
    header = head_path()
    full_path = header + path + str(name)+".csv"
    return full_path

def plotting(name):
    path = configParser("DataPath")['plot_data']
    header = head_path()
    full_path = header + path + str(name)+".csv"
    return full_path

def freq_rate():
    path = configParser("DataPath")['freq_rate']
    fq = int(path)
    return fq

def num_of_batch():
    path = configParser("DataPath")['num_batch']
    nob = int(path)
    return nob

def num_of_exp():
    path = configParser("DataPath")['num_of_exp']
    noe = int(path)
    return noe

def runtime(name):
    path = configParser("DataPath")['runtime']
    header = head_path()
    full_path = header + path + str(name)+".csv"
    return full_path

def falses_num(name):
    path = configParser("DataPath")['falses']
    header = head_path()
    full_path = header + path + str(name)+".csv"
    return full_path
