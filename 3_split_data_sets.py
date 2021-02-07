import argparse
from settings import settings
from face_common import FaceCommon as fc
from util import FaceUtil as fu

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split data sets into train, validation, and test')
    parser.add_argument('--face-dir', default='./faces', help='Full path to the directory with peeople and their names, folder should denote the Name_Surname of the person')
    parser.add_argument('--parts', default=['train', 'ilfw', 'ilfw-test'], help='Parts of splitted dataset')
    parser.add_argument('--portions', default=[80, 10, 10], help='Portions of splitted dataset')
    args = parser.parse_args()

    args = fu.update_face_dir_args(settings, args)
    fc.splits_face_data_sets(args.face_dir, args.parts, args.portions)