"""

  Recognizing the work of:
  
  https://github.com/VictorZhang2014/facenet/blob/master/mydata/generate_pairs.py
  ! encoding: utf-8

"""

import os
import random
from util import CommonUtil as cu
from face_common import FaceCommon as fu


class PairsGenerator:
    """
    Generate the pairs.txt file that is used for training face classifier when calling python `src/train_softmax.py`.
    Or others' python scripts that needs the file of pairs.txt.
    Doc Reference: http://vis-www.cs.umass.edu/lfw/README.txt
    """

    def __init__(self, data_dir, pairs_filepath, img_ext):
        """
        Parameter data_dir, is your data directory.
        Parameter pairs_filepath, where is the pairs.txt that belongs to.
        Parameter img_ext, is the image data extension for all of your image data.
        """
        self.data_dir = data_dir
        self.pairs_filepath = pairs_filepath
        self.img_ext = img_ext
        cu.set_log_verbose(False)
        cu.set_log_prefix('generate_pair.log')

    def generate(self):
        self._generate_matches_pairs()
        self._generate_mismatches_pairs()

    def _generate_matches_pairs(self):
        """
        Generate all matches pairs
        """
        namebar = cu.get_secondary_bar(values=os.listdir(
            self.data_dir), bar_desc="Matching pairs generation progress")
        with open(self.pairs_filepath, "w") as f:
            for name in namebar:
                if name == ".DS_Store":
                    continue
                if not os.path.isdir(name):
                    continue
                path = os.path.join(self.data_dir, name)
                files = os.listdir(path)
                temp = files.copy()
                for i, file in enumerate(files):
                    if file == ".DS_Store":
                        del temp[i]
                for i, file in enumerate(temp):
                    # This line may vary depending on how your images are named.
                    cu.log(f"Generating pair for file {file}")
                    others = temp.copy()
                    if len(others) > 1:
                        del others[i]
                    other = random.choice(others)
                    name, counter = fu.split_face_filename(file)
                    name, other_counter = fu.split_face_filename(other)
                    f.write(name + "\t" + counter + "\t" + other_counter + "\n")
                namebar.refresh()
        namebar.set_description("Matching pairs generation completed")

    def _generate_mismatches_pairs(self):
        """
        Generate all mismatches pairs
        """
        names = os.listdir(self.data_dir)
        namebar = cu.get_secondary_bar(
            values=names, bar_desc="Mismatched pairs generation progress")
        with open(self.pairs_filepath, "a") as f:
            for i, name in enumerate(namebar):
                if name == ".DS_Store":
                    continue
                if not os.path.isdir(name):
                    continue
                curr_path = os.path.join(self.data_dir, name)
                files = os.listdir(curr_path)
                for file in files:
                    temp = names.copy()
                    del temp[i]
                    other = random.choice(temp)
                    other_path = os.path.join(self.data_dir, other)
                    other_file = random.choice(os.listdir(other_path))
                    name, counter = fu.split_face_filename(file)
                    f.write(name + "\t" + counter + "\t")
                    name, counter = fu.split_face_filename(other_file)
                    f.write(name + "\t" + counter + "\t")
                    f.write("\n")
                namebar.update()
                namebar.refresh()
        namebar.set_description("Mismatched pairs generation completed")
