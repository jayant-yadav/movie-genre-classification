#!/usr/bin/env python
# coding: utf-8

# ### Reading the input file and creating a clean one
# Note: only run once

# In[1]:

import shutil
import re
import os

path1 = "./Movie_Poster_Metadata/groundtruth"
temp_path = "./Movie_Poster_Metadata/temp_groundtruth"
path2 = "./Movie_Poster_Metadata/updated_groundtruth"


# In[3]:


def reconstuct_metadata():


    dir_list = os.listdir(path1)

    if not os.path.exists(temp_path):
      os.makedirs(temp_path)    

    if not os.path.exists(path2):
      os.makedirs(path2)
    
    else:
        print("directories already exist. Not cleaning metadata")
        return None

    for file_name in dir_list:

        with open(path1+'/'+file_name,'r',encoding='utf-16-le') as file1:

            temp_file = open(temp_path+'/'+file_name,'w',encoding='utf-8')

            for line in file1.readlines():

                line = line.replace("}\n","},\n")

                # reading all lines that begin with "  "_id""
                y = re.findall("^  \"_id\"", line)
                if not y:
                    temp_file.write(line)

        file1.close()
        temp_file.close()

    dir_list = os.listdir(temp_path)

    for file_name in dir_list:

        with open(temp_path+'/'+file_name,'r',encoding='utf-8') as temp_file:

            file2 = open(path2+'/'+file_name,'w',encoding='utf-8')

            lines = temp_file.readlines()
            lines = lines[1:-1]

            file2.write("[{")
            file2.writelines(lines)
            file2.write("}]")

        temp_file.close()
        file2.close()

    shutil.rmtree(temp_path)  

    return None


# In[ ]:




