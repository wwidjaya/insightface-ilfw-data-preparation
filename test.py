import settings
from face_model import FaceModel

from  settings import faces
import argparse
from google_face_crawler import GoogleFaceCrawler 

parser = argparse.ArgumentParser(description='Data Collection Program for Face Recognition Thesis Project')
# general
parser.add_argument('--silent', default='True', help='Show crawler browser window')
parser.add_argument('--model-prefix', default='./models/model-r50-am-lfw/model', help='The model location prefix ')
parser.add_argument('--model-epoch', default=0, type=int, help='The model epoch')
parser.add_argument('--max-faces', default=100,  type=int, help='Maximum number of faces')
parser.add_argument('--image-size', default='112,112', help='The face image size')
parser.add_argument('--image-path', default='downloads', help='The image download paths')
parser.add_argument('--sleep', default=1,  type=int, help='Sleep between interaction')
parser.add_argument('--model', default='./models/model-r50-am-lfw/model,0', help='path to load model.')
parser.add_argument('--ctx_id', default=0, type=int, help='GPU ID')
parser.add_argument('--chrome-exec-path', default='./modules/chromedriver.exe', help='path to load model.')
args = parser.parse_args()


import cv2

image = './test/anchor.jpeg'
image2 = './test/face 5.jpg'

model = FaceModel(args)

img = cv2.imread(image)
img2 = cv2.imread(image2)

img = model.align_face(img)
img2 = model.align_face(img2)

cv2.imwrite(image + '.jpeg', img)
cv2.imwrite(image2 + '.jpeg', img2)

result, is_similar = model.compare_face(model.get_feature(img), img2)

print("Hasil ", result)
