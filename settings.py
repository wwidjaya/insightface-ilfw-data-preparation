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

import sys
import os
import json


def set_search_path():
  sys.path.insert(1, "./modules")
  sys.path.insert(1, "./dataset")
  os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '0'

def read_setting():

  SETTINGS_FILENAME = "./settings.json"

  settings = {}

  if os.path.exists(SETTINGS_FILENAME):
    with open(SETTINGS_FILENAME, 'r') as f:
      settings = json.load(f)
  return settings

def load_faces():
  filename = cu.get_json_value(settings, 'names.filename', 'face_name_list.dat')
  range = cu.get_json_value(settings, 'names.range', [])
  faces = cu.read_file_as_array(filename)
  if len(range) == 2:    
    start = range[0]
    end = range[1] + 1
    faces = faces[start:end]
  return faces


set_search_path()
from util import CommonUtil as cu

settings = read_setting()
faces = load_faces()
