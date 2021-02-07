from  settings import faces, settings
import argparse
import os
from util import CommonUtil as cu
from face_common import FaceCommon as fc
from util import FaceUtil as fu

parser = argparse.ArgumentParser(description='Data Collection Program for Face Recognition Thesis Project')
parser.add_argument('--image-path', default='./downloads', help='The image download paths')
parser.add_argument('--download-extra-path', default='./downloads-extra', help='The extra image download paths')
parser.add_argument('--face-dir', default='./faces', help='The face processed paths')
parser.add_argument('--face-extra-dir', default='./faces-extra', help='The face processed paths')
parser.add_argument('--check-mode', default="All", help='Check All, downloads and faces')
args = parser.parse_args()

if __name__ == '__main__':
  args = fu.update_face_dir_args(settings, args)
  cu.set_logger("Check Completeness", "check_completeness.log")
  cu.logger.info(f"Total faces count: {len(faces)}")
  cu.logger.info("Checking name list...")
  face_names = []
  extras = []
  cu.logger.info(f"Check Mode: {args.check_mode}")

  ### Checking Missing Directory
  cu.logger.info("Checking missing directory..")
  is_check_download = args.check_mode == "All" or args.check_mode == "Downloads"
  is_check_face = args.check_mode == "All" or args.check_mode == "Faces"
  for i, face in enumerate(faces):
    face_name = fu.get_face_name(face)
    face_names.append(face_name)
    if is_check_download:
      path = os.path.join(args.image_path, face_name)
      if not os.path.exists(path) or not os.path.isdir(path):
        cu.logger.info(" ### Line {}: Download Directory {} for {} not found.".format(i + 1, face_name, face))
    if is_check_face: 
      face_path = os.path.join(args.face_dir, face_name)
      if not os.path.exists(face_path) or not os.path.isdir(face_path):
          cu.logger.info(" ### Line {}: Face Directory {} for {} not found.".format(i + 1, face_path, face))
  cu.logger.info("Finished checking missing directory.")
  
  ### Checking Extra Directory
  cu.logger.info("Checking extra directories...")
  if is_check_download:
    extras = []
    names_on_dir = fc.list_face_names(args.image_path, "")
    for i, name_on_dir in enumerate(names_on_dir):
      found = any(elem == name_on_dir for elem in face_names)
      if not found:
        opath = os.path.abspath(os.path.join(args.image_path, name_on_dir))
        npath= os.path.abspath(os.path.join(args.download_extra_path, name_on_dir))
        cu.logger.info(f"Find extra names {name_on_dir} in the download directory {args.image_path}.")
        os.rename(opath, npath)
        extras.append(name_on_dir)
    extras_count = len(extras)
    if extras_count > 0:
      cu.logger.error(f"Found {extras_count} extra names in the download directory {args.image_path}.")  
  
  if is_check_face:
    extras = []
    names_on_dir = fc.list_face_names(args.face_dir, "")
    for i, name_on_dir in enumerate(names_on_dir):
      found = any(elem == name_on_dir for elem in face_names)
      if not found:
        opath = os.path.abspath(os.path.join(args.face_dir, name_on_dir))
        npath= os.path.abspath(os.path.join(args.face_extra_dir, name_on_dir))
        cu.logger.info(f"Find extra names {name_on_dir} in the face directory {args.face_dir}.")
        os.rename(opath, npath)
        extras.append(name_on_dir)
    extras_count = len(extras)
    if extras_count > 0:
      cu.logger.error(f"Found {extras_count} extra names in the face directory {args.face_dir}")
  cu.logger.info("Checking fiinshed")



    
