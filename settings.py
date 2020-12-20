import sys
sys.path.insert(1, "./modules")
sys.path.insert(1, "./dataset")

from  common import Common
c = Common()
faces = c.read_file_as_array("face_name_list.dat")
