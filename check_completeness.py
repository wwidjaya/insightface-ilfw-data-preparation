from  settings import faces
import argparse
import os
from util import CommonUtil as cu
from face_common import FaceCommon as fc

parser = argparse.ArgumentParser(description='Data Collection Program for Face Recognition Thesis Project')
parser.add_argument('--image-path', default='downloads', help='The image download paths')
parser.add_argument('--face-dir', default='./faces', help='The face processed paths')
args = parser.parse_args()

if __name__ == '__main__':
  cu.log(" Total faces count: {}", len(faces))
  for i, face in enumerate(faces):
    #cu.log("Checking for face {}", face)
    face_dir = fc.get_face_name(face)
    path = os.path.join(args.image_path, face_dir)
    if not os.path.exists(path) or not os.path.isdir(path):
      cu.log(" ### Line {}: Download Directory {} for {} not found.", i + 1, face_dir, face)
    else:
      face_path = os.path.join(args.face_dir, face_dir)
      if not os.path.exists(face_path) or not os.path.isdir(face_path):
          cu.log(" ### Line {}: Face Directory {} for {} not found.", i + 1, face_path, face)


    
