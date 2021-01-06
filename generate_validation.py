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

import os
import settings
from pair_generator import PairsGenerator
import argparse
from lfw2pack import pack_lfw

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate .bin file for validation session')
    parser.add_argument('--face-dir', default='./faces',
                        help='Full path to the directory with peeople and their names, folder should denote the Name_Surname of the person')
    parser.add_argument('--image-ext', default='.jpg',
                        help='Full path to the directory with peeople and their names, folder should denote the Name_Surname of the person')
    parser.add_argument('--parts', default=['ilfw', 'ilfw-test'],
                        help='Parts of validation dataset')
    parser.add_argument('--output-dir',
                        default='./ilfw',
                        help='location of .bin files.')
    parser.add_argument('--image-size', type=str, default='112,112', help='')

    args = parser.parse_args()
    args.face_dir = os.path.abspath(args.face_dir)
    generatePairs = PairsGenerator(args)
    generatePairs.generate()
    pack_lfw(args)
