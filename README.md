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
3. generate_lst.py, by default will generate a .lst file in ./ilfw directory
4. generate_rec.py, by default will generate .rec and .idx file in ./ilfw directory
5. generate_pairs.py, by default will generate pairs.txt file in ./ilfw directory
6. pack_lfw.py, by default will generate .bin file in ./ilfw directory

Notes: ILFW is short for Indonesian Labelled Face in the Wild

## TODO
1. Detail python command
2. More explanation

