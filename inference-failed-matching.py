import settings
import sys
import os
import argparse
import numpy as np
import mxnet as mx
import cv2
import insightface
from insightface.utils import face_align
from face_model import FaceModel

parser = argparse.ArgumentParser(description='Data Collection Program for Face Recognition Thesis Project')
# general
parser.add_argument('--silent', default='True', help='Show crawler browser window')
parser.add_argument('--model-prefix', default='./models/arcface/model', help='The model location prefix ')
parser.add_argument('--model-epoch', default=1, type=int, help='The model epoch')
parser.add_argument('--max-faces', default=30,  type=int, help='Maximum number of faces')
parser.add_argument('--image-size', default='112,112', help='The face image size')
parser.add_argument('--image-path', default='c:\\dataset\\downloads', help='The image download paths')
parser.add_argument('--image-format', default='.jpg', help='The image download paths')
parser.add_argument('--sleep', default=1,  type=int, help='Sleep between interaction')
parser.add_argument('--model', default='./models/model-r50-am-lfw/model,0', help='path to load model.')
parser.add_argument('--gpu', default=-1, type=int, help='GPU ID')
parser.add_argument('--chrome-exec-path', default='./modules/chromedriver.exe', help='path to load model.')
args = parser.parse_args()
args.ctx_id = args.gpu


models = dict()

models['arcface'] =  FaceModel(args, model_root="./models")
args.model_prefix = "./models/ilfw/model"
models['ilfw'] =  FaceModel(args, model_root="./models")
args.model_prefix = "./models/tuned/model"
models['tuned'] =  FaceModel(args, model_root="./models")

###
model = models['ilfw']
one = model.detect_faces(cv2.imread('./test/failed-matching/one.jpg'))[0]
two = model.detect_faces(cv2.imread('./test/failed-matching/two.jpg'))[0]


for name, model in models.items():
    print("\nModel name: ", name)
    print("result: ",  model.compare_image(one, two)[0])
