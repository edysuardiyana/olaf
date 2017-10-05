import numpy as np
import math
from numpy import sqrt
import scipy.stats as st
import timeit
import time

def calc_features(data_vm, data_x, data_y, data_z, freq_rate):

    pre_win = freq_rate
    imp = 2* freq_rate #pre-impact must be 1
    post_win = 3 * freq_rate #pre-impact must be 1
    #print len(data_x)
    #pre-impact
    start_time = timeit.default_timer()# time.clock()
    pre_mean, pre_variance, pre_max_val, pre_min_val, pre_rms, pre_velo, pre_sma, pre_ema, pre_energy = features_calc(data_vm[:pre_win],
    data_x[:pre_win],data_y[:pre_win], data_z[:pre_win], freq_rate)

    #impact_post
    imp_mean, imp_variance, imp_max_val, imp_min_val, imp_rms, imp_velo, imp_sma, imp_ema, imp_energy = features_calc(data_vm[pre_win:imp],
    data_x[pre_win:imp], data_y[pre_win:imp], data_z[pre_win:imp], freq_rate)

     #post impact
    post_mean, post_variance, post_max_val, post_min_val, post_rms, post_velo, post_sma, post_ema, post_energy = features_calc(data_vm[imp:post_win],
    data_x[imp:post_win], data_y[imp:post_win], data_z[imp:post_win], freq_rate)
    end_time = timeit.default_timer() #time.clock()
    run_time = end_time - start_time

    #instance = [pre_mean, pre_variance, pre_max_val, pre_min_val, pre_rms, pre_velo, pre_sma, pre_ema, pre_energy,
    #imp_mean, imp_variance, imp_max_val, imp_min_val, imp_rms, imp_velo, imp_sma, imp_ema, imp_energy,
    #post_mean, post_variance, post_max_val, post_min_val, post_rms, post_velo, post_sma, post_ema, post_energy]

    instance = [pre_mean, pre_sma, pre_velo, pre_ema,
    imp_mean, imp_min_val, imp_rms, imp_velo, imp_sma, imp_ema,
    post_min_val, post_ema]


    return instance, run_time

def features_calc(data,x,y,z,freq_rate):
    new_array = np.array(data)
    mean = round(new_array.mean(),2)
    stdev = round(new_array.std(),2)
    variance = round(np.var(data, ddof=1),2)
    max_val = round(max(data),2)
    min_val = round(min(data),2)
    power_by_two = np.array(data)**2
    means_array = power_by_two.mean()
    rms = round(sqrt(means_array),2)
    raw_velo = integrate(data, freq_rate)
    velo = round(raw_velo,2)
    raw_sma = smafeat(x,y,z,freq_rate)
    sma = round(raw_sma,2)
    raw_ema = ema_calc(data)
    ema = round(raw_ema,2)
    raw_energy = energyCalc(x,y,z, freq_rate)
    energy = round(raw_energy,2)
    return mean, variance, max_val, min_val,rms, velo, sma, ema, energy

def ema_calc(arrdat):
    CONST_ALPHA =  0.01 #float(2)/(len(arrdat)+1) # this is calculated by : 2/N+1 where N is total number of the data
    sem=[]

    for i in range(0,len(arrdat)):

        if i == 0:
            sval = 0

        else:
            sval = (CONST_ALPHA * arrdat[i]) + (1-CONST_ALPHA) * sem[i-1]

        sem.append(sval)


    emval = sem[len(sem)-1]

    return emval

def integrate(arrdat, freq_rate):

    Tperiod = 1/float(freq_rate) #calculate period

    velocity = 0; #initial value of velocity

    for n in range(0,len(arrdat)):

        velocity = velocity + arrdat[n] * Tperiod

    return velocity

def smafeat(datXa,datYa,datZa, freq_rate):

    dataXsq1 = sqrt(np.array(datXa) ** 2)
    dataYsq1 = sqrt(np.array(datYa) ** 2)
    dataZsq1 = sqrt(np.array(datZa) ** 2)


    dataXc1 = integrate(dataXsq1, freq_rate)
    dataYc1 = integrate(dataYsq1, freq_rate)
    dataZc1 = integrate(dataZsq1, freq_rate)
    sma = (dataXc1 + dataYc1 + dataZc1) / float(len(dataXsq1))

    return sma

def energyCalc(array1,array2,array3, freq_rate):

  totEnergy = integrate(np.array(array1) ** 2, freq_rate) + integrate(np.array(array2) ** 2, freq_rate) + integrate(np.array(array3) ** 2, freq_rate)

  return totEnergy
