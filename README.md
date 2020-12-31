# insightface-lfw-data-preparation
Data Preparation Script for Collecting Face Dataset from Google Image Crawler


## Preparation steps:

1. Install required package
if you are not using GPU
pip install mxnet 
or if you are using GPU, please install mxnet-cu92 instead
pip install mxnet-cu92 

pip install selenium
pip install webdriver

2. Before running, you need to list down  the name of famous person that you would like to search from google in a file named face_name_list.dat


## Running the scripts
Run the data preparation script in the following order:

1. collect_faces.py
2. prepare_faces.py
3. generate_lst.py
4. generate_rec.py
5. geenrate_pairs.py
6. pack_lfw.py


