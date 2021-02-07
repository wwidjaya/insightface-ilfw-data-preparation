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
  counts = []
  for face in faces:
    face_name = fu.get_face_name(face, version="2")
    dir = os.path.join(path, face_name)
    if os.path.isdir(dir):
        files = [file for file in os.listdir(dir) if not os.path.isdir(file)]
        count = len(files)
        counts.append(count)
        if count < 5 or count > 50:
          print(f"Found outlier face count for {face} with {count} faces.")
    else:
      print(f"Could not open the {dir} directory ")
  max_count = max(counts)
  min_count = min (counts)
  print(f"Max and min count: {min_count} and {max_count}")

