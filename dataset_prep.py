import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os

import torch
import torch.utils.data as data_utils

from sklearn.preprocessing import MultiLabelBinarizer
import glob
import cv2



### Function to append all the json objects into dataframe

def data_prep():

    dir_list = os.listdir(path2)

    movies_df = pd.DataFrame()

    for file_name in dir_list:    

        df = pd.read_json(path2+'/'+file_name,encoding='utf-8',orient='records')
        df = df[['imdbID','Director','Genre','imdbRating']]
        movies_df = pd.concat([movies_df,df], ignore_index=True)



    return movies_df


### Creating multi-hot encoded genre vectors

def lablel_prep():

    movies_df = data_prep()
    #remove duplicates and set imdbID as index
    movies_df = movies_df.drop_duplicates(subset=["imdbID"], keep="last")
    movies_df.set_index("imdbID", inplace=True)

    mlb = MultiLabelBinarizer()
    multihot = mlb.fit_transform(movies_df["Genre"].dropna().str.split(", "))
    genres_df = pd.DataFrame({"multihot":[multihot.astype(int)]}, index = movies_df.index)
    movies_df = pd.concat([movies_df, genres_df], axis=1 )
    # print(mlb.classes_)
    # print(movies_df.head(10))

    #create a dictionary with multi-hot encoded vectors; index = imdbID
    multihot_dict = {movies_df.index.tolist()[i] : multihot[i] for i in range(0, len(multihot))}
    #print(multihot_dict)
    
    return multihot_dict


def train_test_prep():

    # the data holders
    x_test = []
    x_train = []
    y_test = []
    y_train = []

    #images need to have the same size!!
    flist=glob.glob('./Movie_Poster_Dataset_Cropped_Once/*.jpg')

    length=int(len(flist)*training_size)
    i = 0

    multihot_dict = lablel_prep()
    
    #create lists with input data (images) and output data (multi-hot encoded genre vectors)
    for filename in flist:
            
        imdb_id = filename[filename.index("tt"):filename.index(".jpg")]
        
        if imdb_id in multihot_dict:
            img = np.array(cv2.imread(filename))
            img = np.swapaxes(img, 2,0)
            img = np.swapaxes(img, 2,1)
            
            genre_arr = np.empty([28])
            
            for j in range(len(multihot_dict[imdb_id])):
                genre_arr[j] = multihot_dict[imdb_id][j]
        
            if(i<length):  
                x_train.append(img)
                y_train.append(genre_arr)
            else:
                x_test.append(img)
                y_test.append(genre_arr)
            
            i +=1 

    ##############################################
            #converting the data from lists to numpy arrays
        x_train=np.asarray(x_train,dtype=float)
        x_test=np.asarray(x_test,dtype=float)
        y_train=np.asarray(y_train,dtype=float)
        y_test=np.asarray(y_test,dtype=float)

        #scaling down the RGB data
        x_train /= 255
        x_test /= 255

        #printing stats about the features
        print('x_train shape:', x_train.shape)
        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')

        train_length = x_train.shape[0]

        x_train=torch.from_numpy(x_train)
        x_test=torch.from_numpy(x_test)
        y_train=torch.from_numpy(y_train)
        y_test=torch.from_numpy(y_test)

        train = data_utils.TensorDataset(x_train, y_train)
        train_loader = data_utils.DataLoader(train, batch_size=batch_size, shuffle=True)

        test = data_utils.TensorDataset(x_test, y_test)
        test_loader = data_utils.DataLoader(test, batch_size=batch_size, shuffle=False)

    return None