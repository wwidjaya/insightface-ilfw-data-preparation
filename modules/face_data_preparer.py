# MIT License
#
# Copyright (c) 2020 Wirianto Widjaya
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from util import CommonUtil as cu
from util import ImageUtil as iu
from face_model import FaceModel
from face_common import FaceCommon as fc
import os
import cv2
import numpy as np


class FaceDataPreparer:
  def __init__(self, args):
    args.ctx_id = args.gpu
    self.args = args
    self.model = FaceModel(args, use_large_detector=True)

  
  def valid_file(self, valid_count, face, ext):
    valid_count = valid_count + 1
    image_file = fc.get_file_name(face, valid_count, ext)
    return valid_count, image_file


  def prepare_faces(self, faces):
    for face in faces:
      face = fc.get_face_name(face)
      cu.log("Initiating pre-processing for {}", face)
      path =  os.path.join(self.args.image_path, face).replace(' ', '_')
      output_path =  os.path.join(self.args.output_path, face).replace(' ', '_')

      invalid = os.path.join(path, 'invalid')
      valid = output_path
      duplicate = os.path.join(path, 'duplicate')

      cu.remove_directory(invalid)
      cu.remove_directory(valid)
      cu.remove_directory(duplicate)

      files = cu.listing_directory(path)

      cu.make_directory(self.args.output_path)
      cu.make_directory(invalid)
      cu.make_directory(valid)
      cu.make_directory(duplicate)

      count = 0
      valid_count = 0
      anchor = []
      iu.init_duplicate_check()
      for file in files:
        cu.log("Reading image file {} for pre-processing...", file)
        image = cv2.imread(file)
        count = count + 1
        folder = valid
        splits = os.path.split(file)                  
        image_file = splits[1]
        ext = self.args.file_ext
        if (count == 1):
          cu.log("Reading anchor image {}", file)
          anchor = self.model.get_feature(image)
          valid_count, image_file = self.valid_file(valid_count, face, ext)
        else:
          if iu.is_duplicate(image):
            cu.log("found duplicate image {}", file)
            folder = duplicate
          else:
            cu.log("Comparing image {}", file)
            score, result = self.model.compare_face(anchor, image, low_threshold=0.5)
            if result:
              valid_count, image_file = self.valid_file(valid_count, face, ext)
              print("File ", file,  " sama, hasil: ", score)
            else:
              folder = invalid
              print("File ", file,  " tidak sama, hasil: ", score)
        
        image_file = os.path.join(folder, image_file)
        cv2.imwrite(image_file, image)




  

  
