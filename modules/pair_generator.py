"""

  Recognizing the work of:
  
  https://github.com/VictorZhang2014/facenet/blob/master/mydata/generate_pairs.py
  ! encoding: utf-8

"""

import os
import random
from util import CommonUtil as cu
from util import FaceUtil as fu
from face_common import FaceCommon as fc


class PairsGenerator:
    """
    Generate the pairs.txt file that is used for training face classifier when calling python `src/train_softmax.py`.
    Or others' python scripts that needs the file of pairs.txt.
    Doc Reference: http://vis-www.cs.umass.edu/lfw/README.txt
    """

    def __init__(self, args):
        """
        Parameter data_dir, is your data directory.
        Parameter pairs_filepath, where is the pairs.txt that belongs to.
        Parameter img_ext, is the image data extension for all of your image data.
        """

        self.face_dir = args.face_dir
        self.parts = args.parts
        self.image_ext = args.image_ext
        self.ouput_dir = args.output_dir
        cu.set_logger('Generate Pair','generate_pair.log')

    def generate(self):
        for part in self.parts:
            self._generate_matches_pairs(part)
            self._generate_mismatches_pairs(part)

    def _generate_matches_pairs(self, part):
        """
        Generate all matches pairs
        """
        cu.logger.info(f"Generating matches pairs for {part}...")
        names = fc.list_face_names(self.face_dir, part)
        namebar = cu.get_secondary_bar(values=names, bar_desc="Matching pairs generation progress")
        part_file = os.path.join(self.face_dir, f"{part}-pairs.txt")
        with open(part_file, "w") as f:
            for name in namebar:
                if name == ".DS_Store":
                    continue
                path = os.path.join(self.face_dir, name)
                files = os.listdir(path)
                temp = files.copy()
                for i, file in enumerate(files):
                    if file == ".DS_Store":
                        del temp[i]
                for i, file in enumerate(temp):
                    # This line may vary depending on how your images are named.
                    #cu.logger.info(f"Generating pair for file {file}")
                    others = temp.copy()
                    if len(others) > 1:
                        del others[i]
                    other = random.choice(others)
                    name, counter = fu.split_face_filename(file)
                    name, other_counter = fu.split_face_filename(other)
                    f.write(name + "\t" + counter + "\t" + other_counter + "\n")
                namebar.refresh()
        namebar.set_description("Matching pairs generation completed")
        cu.logger.info(f"Generating matches pairs finished for {part}.")


    def _generate_mismatches_pairs(self, part):
        """
        Generate all mismatches pairs
        """
        cu.logger.info(f"Generating mismatches pairs for {part}...")

        names = fc.list_face_names(self.face_dir, part)
        namebar = cu.get_secondary_bar(
            values=names, bar_desc="Mismatched pairs generation progress")
        part_file = os.path.join(self.face_dir, f"{part}-pairs.txt")
        with open(part_file, "a") as f:
            for i, name in enumerate(namebar):
                if name == ".DS_Store":
                    continue
                curr_path = os.path.join(self.face_dir, name)
                files = os.listdir(curr_path)
                for file in files:
                    temp = names.copy()
                    del temp[i]
                    other = random.choice(temp)
                    other_path = os.path.join(self.face_dir, other)
                    other_file = random.choice(os.listdir(other_path))
                    name, counter = fu.split_face_filename(file)
                    f.write(name + "\t" + counter + "\t")
                    name, counter = fu.split_face_filename(other_file)
                    f.write(name + "\t" + counter + "\t")
                    f.write("\n")
                namebar.update()
                namebar.refresh()
        namebar.set_description("Mismatched pairs generation completed")
        cu.logger.info(f"Generating mismatches pairs for {part} finished.")
