import argparse
import settings
from pair_generator import PairGenerator


if __name__ == '__main__':
    # data_dir = "/home/ti/Downloads/DATASETS/out_data_crop/"
    # pairs_filepath = "/home/ti/Downloads/insightface/src/data/pairs.txt"
    # alternative_lst = "/home/ti/Downloads/insightface/src/data/crop.lst"
    # test_txt = "/home/ti/Downloads/DATASETS/out_data_crop/test.txt"
    # img_ext = ".png"

    # arguments to pass in command line 
    parser = argparse.ArgumentParser(description='Rename images in the folder according to LFW format: Name_Surname_0001.jpg, Name_Surname_0002.jpg, etc.')
    parser.add_argument('--dataset-dir', default='./faces', help='Full path to the directory with peeople and their names, folder should denote the Name_Surname of the person')
    parser.add_argument('--list-file', default='./dataset/ifds.lst', help='Full path to the directory with peeople and their names, folder should denote the Name_Surname of the person')
    parser.add_argument('--img-ext', default='.jpg', help='Full path to the directory with peeople and their names, folder should denote the Name_Surname of the person')
    # reading the passed arguments
    args = parser.parse_args()
    data_dir = args.dataset_dir
    lst = args.list_file
    img_ext = args.img_ext
    # generatePairs = PairGenerator(data_dir, pairs_filepath, img_ext)
    # generatePairs.write_item_label()
    # generatePairs = PairGenerator(data_dir, pairs_filepath, img_ext)
    generatePairs = PairGenerator(data_dir, lst, img_ext)
    generatePairs.write_item_label_abc() # looping through our dataset and creating 1 ITEM_PATH LABEL lst file
    # generatePairs.generate_pairs() # to use, please uncomment this line
    # generatePairs.generate_non_pairs() # to use, please uncomment this line
    
    # generatePairs = PairGenerator(dataset_dir, test_txt, img_ext)
    # generatePairs.split_to_10()