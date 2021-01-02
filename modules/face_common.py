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
from util import CommonUtil as cu


class FaceCommon:

    @staticmethod
    def get_face_name(face):
        face = face.replace(' ', '_')
        names = face.split('_')
        count = len(names)
        if count == 1:
            face = face + '_' + face
        if count >= 3:
            face = names[0] + '_' + names[1]
        return face

    @staticmethod
    def get_file_name(face, counter, ext):
        return FaceCommon.get_face_name(face) + "_" + str(counter).zfill(4) + ext

    @staticmethod
    def get_full_file_name(path, face, counter, ext):
        return os.path.join(path, FaceCommon.get_file_name(face, counter, ext))

    @staticmethod
    def generate_lst_file(data_dir, list_file_name, age):
        names = []
        temp = os.path.split(list_file_name)
        path = temp[0]
        cu.make_directory(path)
        for name in os.listdir(data_dir):
            names.append(name)
        names = sorted(names)
        f = open(list_file_name, 'w')
        for name in names:
            print(name)
            a = []
            for file in os.listdir(data_dir + '/' + name):
                if file == ".DS_Store":
                    continue
                a.append(data_dir + '/' + name + '/' + file)
                f.write(str(1) + '\t' + data_dir + '/' + name +
                        '/' + file + '\t' + str(age) + '\n')
