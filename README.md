# Data Preparation Script for Custom Face Dataset that are collected from Google Image for [InsightFace](https://github.com/deepinsight/insightface) Project

By [Wirianto Widjaya](https://github.com/wwidjaya) 
## Preparation steps:

1. Install required package
if you are not using GPU
```
pip install mxnet 
```
or if you are using GPU, please install mxnet-cu92 instead
```
pip install mxnet-cu92 
```
Install Selenium
```
pip install selenium
```
Install Webdriver
```
pip install webdriver
```
Install insightface
```
pip install insightface
```

2. Before running, you need to list down  the name of famous person that you would like to search from google in a file named face_name_list.dat
## Running the scripts
Run the data preparation script in the following order:

1. collect_faces.py, by default will generate all raw faces into ./downloads directory. You need to make sure that the first file is the anchor image for face comparison to select valid faces in the next steps
2. prepare_faces.py, by default will validate faces and move the valid faces to ./faces directory
3. split_data_sets.py, by default will generate datasets into train, verification, and test (80:10:10), represented by train.part, ilfw.part, and ilfw-test.part file in ./faces directory
4. generate_train.py, by default will generate a train.lst file in ./faces directory, generate train.rec, train.idx, and property file in ./ilfw directory
5. generate_validation.py, by default will generate pairs.txt file in ./faces directory, and generate .bin file in ./ilfw directory

Notes: ILFW is short for Indonesian Labelled Face in the Wild

When properly run, the dataset will create:
1. train.idx
2. train.rec
3. property
4. ilfw.bin
5. ilfw-test.bin

## Before training:

Copy your dataset to folder datasets, and assign your dataset variable for the training as follow:
```
dataset.emore = edict()
dataset.emore.dataset = 'emore'
dataset.emore.dataset_path = '../datasets/ilfw'
dataset.emore.num_classes = <the number of identities>
dataset.emore.image_shape = (112,112,3)
dataset.emore.val_targets = ['ilfw', 'ilfw-test']
```
## TODO
More detailed explanation

