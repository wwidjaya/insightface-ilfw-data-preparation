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

import argparse
import os
import settings
from face2rec import Face2Rec

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='Make a record database by reading from an image list')
parser.add_argument('--prefix',
                    default='./faces',
                    help='prefix of input/output lst and rec files.')
parser.add_argument('--output-dir',
                    default='./ilfw',
                    help='location of lst and rec files.')
cgroup = parser.add_argument_group('Options for creating image lists')
cgroup.add_argument('--exts',
                    nargs='+',
                    default=['.jpeg', '.jpg'],
                    help='list of acceptable image extensions.')
cgroup.add_argument('--chunks',
                    type=int,
                    default=1,
                    help='number of chunks.')
cgroup.add_argument('--train-ratio',
                    type=float,
                    default=1.0,
                    help='Ratio of images to use for training.')
cgroup.add_argument('--test-ratio',
                    type=float,
                    default=0,
                    help='Ratio of images to use for testing.')
cgroup.add_argument(
    '--recursive',
    type=bool,
    default=False,
    help='If true recursively walk through subdirs and assign an unique label\
    to images in each folder. Otherwise only include images in the root folder\
    and give them label 0.')
cgroup.add_argument('--shuffle',
                    type=bool,
                    default=True,
                    help='If this is set as True, \
    im2rec will randomize the image order in <prefix>.lst')

rgroup = parser.add_argument_group('Options for creating database')
rgroup.add_argument(
    '--quality',
    type=int,
    default=95,
    help='JPEG quality for encoding, 1-100; or PNG compression for encoding, 1-9'
)
rgroup.add_argument(
    '--num-thread',
    type=int,
    default=1,
    help='number of thread to use for encoding. order of images will be different\
    from the input list if >1. the input list will be modified to match the\
    resulting order.')
rgroup.add_argument('--color',
                    type=int,
                    default=1,
                    choices=[-1, 0, 1],
                    help='specify the color mode of the loaded image.\
    1: Loads a color image. Any transparency of image will be neglected. It is the default flag.\
    0: Loads image in grayscale mode.\
    -1:Loads image as such including alpha channel.')
rgroup.add_argument('--encoding',
                    type=str,
                    default='.jpg',
                    choices=['.jpg', '.png'],
                    help='specify the encoding of the images.')
rgroup.add_argument(
    '--pack-label',
    type=bool,
    default=False,
    help='Whether to also pack multi dimensional label in the record file')
args = parser.parse_args()
args.prefix = os.path.abspath(args.prefix)
args.output_dir = os.path.abspath(args.output_dir)
Face2Rec.convert_face_2_rec(args)
