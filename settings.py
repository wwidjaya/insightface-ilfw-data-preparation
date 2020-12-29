import sys
import os

sys.path.insert(1, "./modules")
sys.path.insert(1, "./dataset")

from util import CommonUtil as cu
faces = cu.read_file_as_array("face_name_list.dat")

os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '0'
