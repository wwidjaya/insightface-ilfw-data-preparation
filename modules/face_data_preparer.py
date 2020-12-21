from common import Common
import os

class FaceDataPreparer:
  def __init__(self, args):
    self.args = args
    self.c = Common()

  def prepare_faces(self, faces):
    for face in faces:
      path =  os.path.join(self.args.image_path, face).replace(' ', '_')
      files = self.c.listing_directory(path)
      for file in files:
        print(file)
  

  
