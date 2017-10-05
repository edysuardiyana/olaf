from sklearn import preprocessing as pre
import numpy as np
from sklearn.preprocessing import RobustScaler

def norm_feat(arr):

    new_arr = np.array(arr)

    scaled_data = RobustScaler().fit_transform(new_arr)

    return scaled_data

def main():

    arr = [[1.,-1.,2.],[2.,0.,0.,],[0.,1.,-1.,]]
    new_arr = norm_feat(arr)

    print new_arr

if __name__ == '__main__':
    main()
