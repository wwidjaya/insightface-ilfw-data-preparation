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

model = models['arcface']
frontal = model.detect_faces(cv2.imread('./test/frontal.jpg'))[0]
masked = model.detect_faces(cv2.imread('./test/masked.jpg'))[0]
masked_green = model.detect_faces(cv2.imread('./test/masked_green.jpg'))[0]
no_glasses = model.detect_faces(cv2.imread('./test/no-glasses.jpg'))[0]
side = model.detect_faces(cv2.imread('./test/side.jpg'))[0]
up = model.detect_faces(cv2.imread('./test/up.jpg'))[0]
down = model.detect_faces(cv2.imread('./test/down.jpg'))[0]
diff = model.detect_faces(cv2.imread('./test/different.jpg'))[0]
light = model.detect_faces(cv2.imread('./test/lighting.jpg'))[0]

jeff = model.detect_faces(cv2.imread('./test/jeff.jpg'))[0]
kurt = model.detect_faces(cv2.imread('./test/kurt.jpg'))[0]

cv2.imwrite('./test/frontal-aligned.jpg', frontal)
cv2.imwrite('./test/masked-aligned.jpg', masked)
cv2.imwrite('./test/masked-green-aligned.jpg', masked_green)
cv2.imwrite('./test/no_glasses-aligned.jpg', no_glasses)
cv2.imwrite('./test/side-aligned.jpg', side)
cv2.imwrite('./test/up-aligned.jpg', up)
cv2.imwrite('./test/down-aligned.jpg', down)
cv2.imwrite('./test/different-aligned.jpg', diff)
cv2.imwrite('./test/lighting-aligned.jpg', light)
cv2.imwrite('./test/jeff-aligned.jpg', jeff)
cv2.imwrite('./test/kurt-aligned.jpg', kurt)



for name, model in models.items():
    print("\nModel name: ", name)
    print("frontal to frontal: ",  model.compare_image(frontal, frontal)[0])
    print("frontal to masked: ",  model.compare_image(frontal, masked)[0])
    print("frontal to masked_green: ",  model.compare_image(frontal, masked_green)[0])
    print("masked to masked_green: ",  model.compare_image(masked, masked_green)[0])
    print("frontal to no glasses: ",  model.compare_image(frontal, no_glasses)[0])
    print("frontal to side: ",  model.compare_image(frontal, side)[0])
    print("frontal to up: ",  model.compare_image(frontal, up)[0])
    print("frontal to down: ",  model.compare_image(frontal, down)[0])
    print("frontal to different: ",  model.compare_image(frontal, diff)[0])
    print("frontal to lighting: ",  model.compare_image(frontal, light)[0])
    print("jeff to kurt: ",  model.compare_image(frontal, light)[0])
