from  settings import faces
import argparse
import os
from util import FaceUtil as fu

parser = argparse.ArgumentParser(description='Data Collection Program for Face Recognition Thesis Project')
# general
parser.add_argument('--image-path', default='./faces/without-mask', help='The image download paths')
args = parser.parse_args()

if __name__ == '__main__':
  path = args.image_path
  for face in faces:
    face_name = fu.get_face_name(face, version="2")
    dir = os.path.join(path, face_name)
    if os.path.isdir(dir):
        files = [file for file in os.listdir(dir) if not os.path.isdir(file)]
        for file in files:
          name, counter = fu.split_face_filename(file)
          if not name == face_name:
            new_name = file.replace(name, face_name)
            opath = os.path.join(dir, file)
            npath = os.path.join(dir, new_name)
            os.rename(opath, npath)
            print(f"Found inconsistent {file} supposed to be {new_name}.")
    else:
      print(f"Could not open the {dir} directory ")


