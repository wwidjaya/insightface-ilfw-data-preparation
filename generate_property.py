import argparse
import settings
from face_common import FaceCommon as fc

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename images in the folder according to LFW format: Name_Surname_0001.jpg, Name_Surname_0002.jpg, etc.')
    parser.add_argument('--dataset-dir', default='./faces', help='Full path to the directory with peeople and their names, folder should denote the Name_Surname of the person')
    parser.add_argument('--prop-file', default='./ilfw/property', help='Full path to the directory with peeople and their names, folder should denote the Name_Surname of the person')
    
    args = parser.parse_args()
    data_dir = args.dataset_dir
    prop = args.prop_file
    fc.generate_property_file(data_dir, prop)