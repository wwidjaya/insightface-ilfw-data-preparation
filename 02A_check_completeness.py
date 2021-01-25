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
  cu.log(" Checking name list...")
  face_names = []
  extras = []
  for i, face in enumerate(faces):
    #cu.log("Checking for face {}", face)
    face_dir = fc.get_face_name(face)
    face_names.append(face_dir)
    path = os.path.join(args.image_path, face_dir)
    if not os.path.exists(path) or not os.path.isdir(path):
      cu.log(" ### Line {}: Download Directory {} for {} not found.", i + 1, face_dir, face)
    else:
      face_path = os.path.join(args.face_dir, face_dir)
      if not os.path.exists(face_path) or not os.path.isdir(face_path):
          cu.log(" ### Line {}: Face Directory {} for {} not found.", i + 1, face_path, face)
  cu.log(" Checking directories...")
  names_on_dir = fc.list_face_names(args.image_path, "")
  for i, name_on_dir in enumerate(names_on_dir):
    found = any(elem == name_on_dir for elem in face_names)
    if not found:
      cu.log(f"Find extra names {name_on_dir} in the download directory {args.image_path}.")
      extras.append(name_on_dir)
  extras_count = len(extras)
  if extras_count > 0:
    cu.log(f"Found {extras_count} extra names in the download directory {args.image_path}")  
  extras = []
  names_on_dir = fc.list_face_names(args.face_dir, "")
  for i, name_on_dir in enumerate(names_on_dir):
    found = any(elem == name_on_dir for elem in face_names)
    if not found:
      cu.log(f"Find extra names {name_on_dir} in the directory {args.face_dir}.")
      extras.append(name_on_dir)
  extras_count = len(extras)
  if extras_count > 0:
    cu.log(f"Found {extras_count} extra names in the face directory {args.face_dir}")
  cu.log(" Checking fiinshed")



    
