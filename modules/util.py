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

import sys

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("process.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    

sys.stdout = Logger()

class ImageUtil:

  images = []

  @staticmethod
  def init_duplicate_check():
    ImageUtil.images = []

  @staticmethod
  def is_duplicate(image):
    hash = ImageUtil.dhash(image)
    found = any(elem == hash for elem in ImageUtil.images)
    if not found:
      ImageUtil.images.append(hash)
    return found

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
    return np.zeros([100,100,3],dtype=np.uint8)

class CommonUtil:

  def __init__(self):
    None

  @staticmethod
  def remove_file(path:str):
    try:
      os.remove(path)
    except:
      pass


  @staticmethod
  def remove_directory(path:str):
    try:
      if os.path.exists(path):
        shutil.rmtree(path)
    except:
      print("")

  @staticmethod
  def make_directory(path:str):
      if not os.path.exists(path):
          os.mkdir(path)

  @staticmethod
  def log(string:str, *args):
    print("{}:{}".format(datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"), string.format(*args)))

  @staticmethod
  def timing(action):
      start_time = time.time()
      CommonUtil.log("Starting {}", action)
      return lambda x: CommonUtil.log("[{:.2f}s] {} finished{}", time.time() - start_time, action, x)

  @staticmethod
  def get_file_ext_from_url(url:str):
    p = urlparse(url)
    return os.path.splitext(p.path)[1]

  @staticmethod
  def get_file_ext(filename:str):
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
      files.append(os.path.join(folder,filename))
    return files
      

