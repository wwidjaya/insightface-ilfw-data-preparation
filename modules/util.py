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

import time
import datetime
from urllib.parse import urlparse
import os
import cv2
import shutil
import sys
import numpy as np
import pathlib
from tqdm import tqdm


import sys
class ImageUtil:

    images = []

    @staticmethod
    def init_duplicate_check():
        ImageUtil.images = []

    @staticmethod
    def is_duplicate(image):
        is_valid = True
        found = False
        try:
            hash = ImageUtil.dhash(image)
            found = any(elem == hash for elem in ImageUtil.images)
            if not found:
                ImageUtil.images.append(hash)
        except Exception as e:
            is_valid = False
        return found, is_valid

    @staticmethod
    def dhash(image, hashSize=8):
        # resize the input image, adding a single column (width) so we
        # can compute the horizontal gradient
        resized = cv2.resize(image, (hashSize + 1, hashSize))
        # compute the (relative) horizontal gradient between adjacent
        # column pixels
        diff = resized[:, 1:] > resized[:, :-1]
        # convert the difference image to a hash
        return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

    @staticmethod
    def get_blank_image():
        return np.zeros([100, 100, 3], dtype=np.uint8)


class CommonUtil:

    def __init__(self):
        pass

    @staticmethod
    def set_logger(id, filename):
        import os
        import logging, logging.handlers
        import time


        os.environ['TZ'] = 'Asia/Jakarta'
        if not os.name == 'nt':
            time.tzset()

        CommonUtil.logger = logging.getLogger(id)
        CommonUtil.logger.setLevel(logging.INFO)
        dp = CommonUtil.get_date_prefix()
        path = os.path.join("./logs", f"{dp}-{filename}")
        handler = logging.handlers.RotatingFileHandler(path, maxBytes=500000, backupCount=5)
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)-8s: %(message)s')
        handler.setFormatter(formatter)
        logging.Formatter.converter = time.gmtime
        CommonUtil.logger.addHandler(handler)
        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)-8s: %(message)s')
        console.setFormatter(formatter)
        CommonUtil.logger.addHandler(console)


    @staticmethod
    def set_log_verbose(value):
        CommonUtil.logger.propagate = value

    @staticmethod
    def get_primary_bar(values, bar_desc='Overall progress'):
        return tqdm(values, leave=False, position=1, desc=bar_desc)

    @staticmethod
    def get_secondary_bar(values=None, bar_total=None, bar_desc=''):
        bar = None
        if values is not None:
            bar = tqdm(values, leave=True, position=0, desc=bar_desc)
        else:
            if bar_total is not None:
                bar = tqdm(total=bar_total, leave=True,
                           position=0,  desc=bar_desc)
        return bar

    @staticmethod
    def remove_file(path: str):
        try:
            os.remove(path)
        except:
            pass

    @staticmethod
    def remove_directory(path: str):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
        except:
            print("")

    @staticmethod
    def make_directory(path: str):
        if not os.path.exists(path):
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_date_prefix():
        return datetime.datetime.now().strftime("%Y.%m.%d %H%M%S")

    @staticmethod
    def timing(action):
        start_time = time.time()
        CommonUtil.logger.info("Starting {action}")
        return lambda x: CommonUtil.logger.info("[{:.2f}s] {} finished{}".format(time.time() - start_time, action, x))

    @staticmethod
    def get_file_ext_from_url(url: str):
        p = urlparse(url)
        return os.path.splitext(p.path)[1]

    @staticmethod
    def get_file_ext(filename: str):
        return os.path.splitext(filename)[1]

    @staticmethod
    def read_file_as_array(filename):
        lines = []
        with open(filename) as fp:
            for line in fp:
                lines.append(line.strip())
        return lines

    @staticmethod
    def listing_directory(folder):
        files = []
        for filename in os.listdir(folder):
            files.append(os.path.join(folder, filename))
        return files

    @staticmethod
    def get_json_value(json_value, key_string: str, default):
        value = default
        try:
            keys = key_string.split('.')
            for key in keys:
                json_value = json_value[key]
            value = json_value
        except Exception as e:
            pass
        return value

    @staticmethod
    def blocks(files, size=65536):
        while True:
            b = files.read(size)
            if not b:
                break
            yield b

    @staticmethod
    def count_line_in_file(filename:str):
        with open(filename, "r", encoding="utf-8", errors='ignore') as f:
            count = (sum(bl.count("\n") for bl in CommonUtil.blocks(f)))
        return count

class FaceUtil:
   
    @staticmethod
    def split_face_filename(path):
        file = os.path.split(path)[1]
        filename = os.path.splitext(file)
        splits = filename[0].split('_')
        split_length = len(splits)
        name = ''
        counter = ''
        for i, split in enumerate(splits):
            if i == 0:
                name = split
            else:
                if (i + 1) == split_length:
                    counter = split.strip('0')
                else:
                    name = name + '_' + split

        return name, counter
    
    @staticmethod
    def get_face_name(face, version="2"):
        face = face.replace(' ', '_')
        if version == "1":
            names = face.split('_')
            count = len(names)
            if count == 1:
                face = face + '_' + face
            if count >= 3:
                face = ''
                counter = 0
                for name in names:
                    counter = counter + 1
                    if counter == count:
                        face = face + '_' + name
                    else:
                        face = face + name[:1]
    
        if version == "2":
            face = face.replace('.', '').replace(',', '')
            names = face.split('_')
            count = len(names)
            if count == 1:
                face = face + '_' + face
            if count >= 3:
                face = ''
                counter = 0
                for name in names:
                    counter = counter + 1
                    if counter == 1: 
                        face = name
                    else:
                        if counter <= 2 or counter == count:
                            face = face + '_' + name
                        else:
                            face = face + '_' + name[:1]
        return face

    @staticmethod
    def get_file_name(face, counter, ext, version="2"):
        return FaceUtil.get_face_name(face, version) + "_" + str(counter).zfill(4) + ext

    @staticmethod
    def get_full_file_name(path, face, counter, ext, version="2"):
        return os.path.join(path, FaceUtil.get_file_name(face, counter, ext, version))    

    @staticmethod
    def update_face_dir_args(settings, args):
        is_mask = CommonUtil.get_json_value(settings, 'faces.with-mask', "True")
        mask_folder = CommonUtil.get_json_value(settings, 'faces.mask-folder', "with-mask")
        without_mask_folder = CommonUtil.get_json_value(settings, 'faces.without-mask-folder', "without-mask")
        folder = mask_folder
        if not is_mask == "True":
            folder = without_mask_folder
        if hasattr(args, 'face_dir'):
            args.face_dir = os.path.join(args.face_dir, folder)
        if hasattr(args, 'output_path'):
            args.output_path = os.path.join(args.output_path, folder)
        if hasattr(args, 'face_extra_dir'):
            args.face_extra_dir = os.path.join(args.face_extra_dir, folder)
        return args
     