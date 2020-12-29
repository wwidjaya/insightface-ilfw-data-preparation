import os

class FaceCommon:
  
  @staticmethod
  def get_file_name(face, counter, ext):
    return face.replace(" ", "_") + "_" + str(counter).zfill(4) + ext

  @staticmethod
  def get_full_file_name(path, face, counter, ext):
    return os.path.join(path, face.replace(" ", "_") + "_" + str(counter).zfill(4) + ext)
