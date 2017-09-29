import features_eves as ft_stage
import math
import operator
import matplotlib.pyplot as plt
import timeit
import time


FALL_FORWARD = 2
FALL_BACKWARD = 6
FALL_LEFT = 10
FALL_RIGHT = 11
FALL_BLIND_FORWARD = 12
FALL_BLIND_BACKWARD = 13
THRESHOLD = 1.8
FALL_SET = set([FALL_FORWARD,
                FALL_BACKWARD,
                FALL_LEFT,
                FALL_RIGHT,
                FALL_BLIND_FORWARD,
                FALL_BLIND_BACKWARD])


def eves_window(data_x, data_y, data_z, annot, freq_rate,name):
    size_active_win = 2 * freq_rate # 1 is the size of pre-impact window
    feature_win = 3 * freq_rate # 1 is the size of pre-impact window
    buffer_size = freq_rate
    buffer_x = []
    buffer_y = []
    buffer_z = []
    buffer_vm= []
    buffer_annot = []
    annot_num = 0
    annot_flag = 0
    run_time_seq = []
    instances_seq = []

    temp_max = 0
    index_temp_2 = 0
    temp_max_2 = THRESHOLD
    state_1 = False
    state_2 = False
    state_3 = False

    state_2_flag = False

    trans_1 = 0
    trans_2 = 0
    trans_3 = 0
    trans_4 = 0
    trans_5 = 0
    trans_6 = 0
    trans_7 = 0
    trans_8 = 0
    trans_9 = 0
    nd_1 = 0
    nd_2 = 0
    nd_3 = 0
    for i in range(0,len(data_x)):
        #print "data number : "+str(i)

        buffer_x.append(data_x[i])
        buffer_y.append(data_y[i])
        buffer_z.append(data_z[i])
        svm_val = l2norm(data_x[i], data_y[i], data_z[i])
        buffer_vm.append(svm_val)
        buffer_annot.append(annot[i])

        #print buffer_vm
        if not state_1:
            if len(buffer_vm) == buffer_size + 1:
                state_1 = True
            else:
                state_1 = False

        if state_1:
            nd_1 = nd_1 + 1
            #print "state 1"
            state_2_flag = False
            if round(buffer_vm[len(buffer_vm)-1],1) >= THRESHOLD:
                trans_2 = trans_2 + 1
                state_2 = True
                state_1 = False
                temp_max = buffer_vm[len(buffer_vm)-1]
            else:
                trans_1 = trans_1 + 1
                del buffer_vm[0]
                del buffer_x[0]
                del buffer_y[0]
                del buffer_z[0]
                del buffer_annot[0]
                state_1 = False

        elif state_2:
            #print "state 2"
            state_2_flag = False
            nd_2 = nd_2 + 1
            if round(buffer_vm[len(buffer_vm)-1],1) > temp_max:
                trans_3 = trans_3 + 1
                temp_max = buffer_vm[len(buffer_vm)-1]
                del buffer_vm[:len(buffer_vm)-(buffer_size + 1)]
                del buffer_x[:len(buffer_x)-(buffer_size + 1)]
                del buffer_y[:len(buffer_y)-(buffer_size + 1)]
                del buffer_z[:len(buffer_z)-(buffer_size + 1)]
                del buffer_annot[:len(buffer_annot)-(buffer_size + 1)]
            else:
                trans_4 = trans_4 + 1
                if len(buffer_vm) >= size_active_win: #changed to >=
                    trans_5 = trans_5 + 1
                    state_2 = False
                    state_3 = True
        elif state_3 :
            #print "state 3"
            nd_3 = nd_3 + 1
            if len(buffer_vm) >= feature_win + 1: #changed to >=
                if len(buffer_vm[:len(buffer_vm)-1])!=feature_win:
                    print "here we are"

                instance, runtime = ft_stage.calc_features(
                buffer_vm[:len(buffer_vm)-1],
                buffer_x[:len(buffer_x)-1],
                buffer_y[:len(buffer_y)-1],
                buffer_z[:len(buffer_z)-1],
                freq_rate)


                instance.append(buffer_annot[freq_rate])

                if buffer_annot[freq_rate] in FALL_SET:
                    instance.append(1)
                else:
                    instance.append(0)

                instances_seq.append(instance)
                run_time_seq.append(runtime)

                temp_max = temp_max_2
                if state_2_flag:
                    trans_6 = trans_6 + 1
                    state_2 = True
                    del buffer_vm[:index_temp_2 - buffer_size]
                    del buffer_x[:index_temp_2 - buffer_size]
                    del buffer_y[:index_temp_2 - buffer_size]
                    del buffer_z[:index_temp_2 - buffer_size]
                    del buffer_annot[:index_temp_2 - buffer_size]
                else:
                    trans_9 = trans_9 + 1
                    del buffer_vm[:len(buffer_vm) - buffer_size]
                    del buffer_x[:len(buffer_x) - buffer_size]
                    del buffer_y[:len(buffer_y) - buffer_size]
                    del buffer_z[:len(buffer_z) - buffer_size]
                    del buffer_annot[:len(buffer_annot) - buffer_size]

                    state_1 = True
                temp_max_2 = THRESHOLD #resetting temp_max_2
                state_3 = False
            else:
                trans_7 = trans_7 + 1
                if round(buffer_vm[len(buffer_vm)-1],1) > temp_max_2 and round(buffer_vm[len(buffer_vm)-1],1)>= THRESHOLD:
                    trans_8 = trans_8 + 1
                    temp_max_2 = buffer_vm[len(buffer_vm)-1]
                    index_temp_2 = len(buffer_vm)-1
                    state_2_flag = True

    state_stats = [nd_1, nd_2, nd_3, trans_1, trans_2, trans_3, trans_4, trans_5, trans_6, trans_7, trans_8, trans_9]
    return instances_seq,run_time_seq, state_stats

def l2norm(x, y, z):
    return math.sqrt(x * x + y * y + z * z)
