from  settings import faces
from face_data_preparer import FaceDataPreparer
import argparse


parser = argparse.ArgumentParser(description='Data Preparer Program for Face Recognition Thesis Project')
# general
parser.add_argument('--model-prefix', default='./models/model-r50-am-lfw/model', help='The model location prefix ')
parser.add_argument('--model-epoch', default=0, type=int, help='The model epoch')
parser.add_argument('--image-size', default='112,112', help='The face image size')
parser.add_argument('--image-path', default='./downloads', help='The image download paths')
parser.add_argument('--model', default='./models/model-r50-am-lfw/model,0', help='path to load model.')
parser.add_argument('--gpu', default=-1, type=int, help='GPU ID')
args = parser.parse_args()

if __name__ == '__main__':  
  fdp = FaceDataPreparer(args)
  fdp.prepare_faces(faces)
