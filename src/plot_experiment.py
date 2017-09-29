import source_reader as src
import statistics as st
import matplotlib.pyplot as plt


def main_plot(noe,cl):
    all_data = []
    for i in range(noe):
        temp_data = read_plot(i,cl)
        all_data.append(temp_data)

    plot_dat = modify(all_data,noe)
    #print len(plot_dat)
    #plt.plot(plot_dat)
    #plt.show()

    return plot_dat

def read_plot(noe,cl):
    filename = 'cl_'+str(cl)+'_result_'+str(noe)
    path = src.result(filename)
    data = []
    with open(path) as obj:
        for line in obj:
            raw = line.split()
            raw_fl = [float(i) for i in raw[:len(raw)]]
            data.append(raw_fl[7])

    return data


def modify(data, noe):
    fin_data = []
    for i in range(len(data[0])):
        temp_row = []
        for j in range(noe):
            temp_row.append(data[j][i])

        mean_dat = round(st.mean(temp_row),1)
        fin_data.append(mean_dat)

    return fin_data
