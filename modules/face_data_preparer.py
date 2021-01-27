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
from util import FaceUtil as fu
import os
import cv2

class FaceDataPreparer:
  def __init__(self, args):
    args.ctx_id = args.gpu
    self.args = args
    self.model = FaceModel(args, use_large_detector=True)
  
  def valid_file(self, valid_count, face, ext):
    valid_count = valid_count + 1
    image_file = fu.get_file_name(face, valid_count, ext)
    return valid_count, image_file


  def prepare_faces(self, faces):
    facebar = cu.get_primary_bar(faces)
    for face in facebar:
      face = fu.get_face_name(face)
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
      facebar.refresh()
      filebar = cu.get_secondary_bar(files)
      for file in filebar:
        cu.log(f"Reading image file {file} for pre-processing...")
        image = cv2.imread(file)
        count = count + 1
        folder = valid
        splits = os.path.split(file)                  
        image_file = splits[1]
        filebar.set_description(f"Processing {image_file}")
        ext = self.args.file_ext
        if (count == 1):
          cu.log("Reading anchor image {}", file)
          anchor = self.model.get_feature(image)
          valid_count, image_file = self.valid_file(valid_count, face, ext)
        else:
          is_found, is_valid = iu.is_duplicate(image)
          if not is_valid:
              folder = invalid
              image = iu.get_blank_image()
              cu.log(f"File {file} tidak valid.")
          else:
            if is_found:
              cu.log("found duplicate image {}", file)
              folder = duplicate
            else:
              cu.log("Comparing image {}", file)
              score, result = self.model.compare_face(anchor, image, low_threshold=0.5)
              if result:
                valid_count, image_file = self.valid_file(valid_count, face, ext)
                cu.log(f"File {file} sama, hasil: {score}")
              else:
                folder = invalid
                cu.log(f"File {file} tidak sama, hasil: {score}")
        filebar.set_description(desc=f"Process for {face} is finished.", refresh=True)
        
        image_file = os.path.join(folder, image_file)
        cv2.imwrite(image_file, image)
    
  def check_duplicate_faces(self, faces):
    cu.set_log_verbose(False)
    cu.set_log_prefix("check_duplicate_face.log")
    facebar = cu.get_secondary_bar(faces)
    faces_features = []
    names = []
    cu.log("Reading face feature....")
    for face in facebar:
      face_name = fu.get_face_name(face)
      names.append(face_name)
      path =  os.path.join(self.args.image_path, face_name)
      file = [x for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x))][0]
      file_path = os.path.join(path, file)
      #cu.log("checking {} got {}", path, file_path)
      feature = self.model.get_feature(cv2.imread(file_path))
      faces_features.append(feature)
      facebar.set_description(f"Reading {face}")
      facebar.refresh()
    cu.log("Comparing face feature....")
    duplicates = []
    for i, name in enumerate(names):
      #cu.log(f"Checking duplicate on {name}..")
      for x, feature in enumerate(faces_features):
        if not i == x:
          result, is_similar = self.model.compare_feature(faces_features[i], faces_features[x])
          if is_similar:
            ori_name = faces[x]
            dup_face = faces[i]
            cu.log(f"Find duplicate face for {ori_name} in line {x}, with {dup_face} in line {i}")
            duplicate = {}
            duplicate["name"] = ori_name
            duplicate["with"] = dup_face  
            duplicates.append(duplicate)
    dup_count = len(duplicates)
    if dup_count > 0:
      cu.set_log_verbose(True)
      cu.log(f"Found {dup_count} duplicate face in the download directory {self.args.image_path}")
      print(duplicates)
    cu.log("Detecting duplicate face finished.")

      
  def apply_mask_to_faces(self, faces):
      cu.set_log_verbose(False)
      cu.set_log_prefix("apply_mask_to_face.log")
      facebar = cu.get_secondary_bar(faces)
      names = []
      cu.log("Reading faces....")
      for face in facebar:
        face_name = fu.get_face_name(face)
        names.append(face_name)
        path =  os.path.join(self.args.output_path, face_name)
        files = [x for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x))]
        file_count = len(files)
        mask_count = int(self.args.max_percent_masks/100*file_count)
        if mask_count < 1: 
          mask_count = 1
        for x in range(mask_count):
          file_path = os.path.join(path, files[x])
          mask_path = fu.get_full_file_name(path, face, file_count + x + 1, self.args.file_ext)
          fc.apply_mask(file_path, masked_file_path=mask_path)
          facebar.set_description(f"Applying mask to {file_path} as {mask_path}")
          facebar.refresh()
      cu.log("Apply face mask finished.")


  

  
