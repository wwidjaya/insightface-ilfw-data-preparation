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
    def split_face_filename(path):
        file = os.path.split(path)[1]
        filename = os.path.splitext(file)
        splits = filename[0].split('_')
        name = splits[0] + '_' + splits[1]
        counter = splits[2].lstrip('0')
        return name, counter


    @staticmethod
    def get_face_name(face):
        face = face.replace(' ', '_')
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
                    face = face + '_' + names[counter - 1]
                else:
                    face = face + name[:1] 
        return face

    @staticmethod
    def get_file_name(face, counter, ext):
        return FaceCommon.get_face_name(face) + "_" + str(counter).zfill(4) + ext

    @staticmethod
    def get_full_file_name(path, face, counter, ext):
        return os.path.join(path, FaceCommon.get_file_name(face, counter, ext))

    @staticmethod
    def generate_lst_file(data_dir, list_file_name, age):
        cu.set_log_prefix('generate_lst.log')
        cu.set_log_verbose(False)
        cu.log("Generating list file")
        names = []
        temp = os.path.split(list_file_name)
        path = temp[0]
        cu.make_directory(path)
        for name in os.listdir(data_dir):
            cu.log(f"Adding name {name} to list file")
            names.append(name)
        names = sorted(names)
        f = open(list_file_name, 'w')
        name_bar = cu.get_secondary_bar(values=names, bar_desc='Overall progress')
        for name in name_bar:
            a = []
            for file in os.listdir(data_dir + '/' + name):
                cu.log(f"Processing {file}")
                name_bar.set_description(f"Processing {file}")
                if file == ".DS_Store":
                    continue
                a.append(data_dir + '/' + name + '/' + file)
                f.write(str(1) + '\t' + data_dir + '/' + name +
                        '/' + file + '\t' + str(age) + '\n')
            name_bar.set_description(f"Processing finished")


    @staticmethod
    def generate_property_file(data_dir, property_file_name):
        cu.set_log_prefix('generate_prop.log')
        cu.log("Generating property file")
        count = len(os.listdir(data_dir))
        f = open(property_file_name, 'w')
        f.write(f"{count},112,112")
        cu.log('Property file generated')
