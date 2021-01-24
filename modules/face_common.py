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
import random
from face_masker import FaceMasker
from settings import all_faces

class FaceCommon:

    @staticmethod
    def apply_mask(image_path, mask_path='./images/blue-mask.png'):
        show = False
        model = "hog"
        FaceMasker(image_path, mask_path, show, model).mask()

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
    def generate_lst_file(face_dir, list_file_name, age):
        cu.set_log_prefix('generate_lst.log')
        cu.set_log_verbose(False)
        cu.log("Generating list file")
        names = []
        temp = os.path.split(list_file_name)
        path = temp[0]
        cu.make_directory(path)
        names = FaceCommon.list_face_names(face_dir)
        f = open(list_file_name, 'w')
        name_bar = cu.get_secondary_bar(
            values=names, bar_desc='Overall progress')
        for name in name_bar:
            a = []
            for file in os.listdir(face_dir + '/' + name):
                cu.log(f"Processing {file}")
                name_bar.set_description(f"Processing {file}")
                if file == ".DS_Store":
                    continue
                a.append(face_dir + '/' + name + '/' + file)
                f.write(str(1) + '\t' + face_dir + '/' + name +
                        '/' + file + '\t' + str(age) + '\n')
            name_bar.set_description(f"Processing finished")

    @staticmethod
    def list_face_names(face_dir, part="train"):
        names = []
        if not part == "":
            part_file = os.path.join(face_dir, f"{part}.part")
            parts = cu.read_file_as_array(part_file)
            ignored = [".DS_Store"]
            names = [x for x in os.listdir(
                face_dir) if x in parts and x not in ignored]
        else:
            folders = os.listdir(face_dir)
            for folder in folders:
                full_path = os.path.join(face_dir, folder)
                if os.path.isdir(full_path):
                    names.append(folder)
        return sorted(names)

    @staticmethod
    def generate_property_file(face_dir, property_file_name):
        cu.set_log_prefix('generate_prop.log')
        cu.log("Generating property file")
        count = len(FaceCommon.list_face_names(face_dir))
        f = open(property_file_name, 'w')
        f.write(f"{count},112,112")
        cu.log('Property file generated')

    @staticmethod
    def splits_face_data_sets(face_dir, parts=['train', 'ilfw', 'ilfw-test'], portions=[80, 10, 10]):
        cu.set_log_prefix('split_face_data_sets.log')
        cu.log("Splitting face dataset")
        names = FaceCommon.list_face_names(face_dir, part="")
        random.shuffle(names)
        count = len(names)
        counts = []
        part_count = len(parts)
        running_count = 1
        for i, portion in enumerate(portions):
            part = parts[i]
            if i < (part_count - 1):
                current_count = int(round(portion/100 * count, 0))
            else:
                current_count = count - running_count
            start = running_count - 1
            end = running_count + current_count - 1
            lines = names[start: end]
            f = open(os.path.join(face_dir, f"{part}.part"), 'w')
            for line in lines:
                f.write(f"{line}\n")
            f.close()
            running_count = running_count + current_count
            counts.append(current_count)
        cu.log('Face splitting finished')

    @staticmethod
    def check_name_list():
        cu.set_log_verbose(False)
        cu.set_log_prefix('check_names.log')
        facebar = cu.get_secondary_bar(all_faces)
        face_names = []
        face_list = {}
        duplicates = []
        counter = 0
        for face in facebar:
            facebar.set_description(f"Checking {face}")
            facebar.refresh()
            face_name = FaceCommon.get_face_name(face)
            found = any(elem == face_name for elem in face_names)
            if found:
                dup = face_list[face_name]["name"]
                dup_pos = face_list[face_name]["pos"]
                line = counter+1
                cu.log(f"Line {line}: Find duplicate {face} with {dup} in line {dup_pos}, for face name {face_name}")
                duplicates.append(face_name)
            face_list[face_name] = {}
            face_list[face_name]["name"] = face
            face_list[face_name]["pos"] = counter + 1
            face_names.append(face_name)
            facebar.set_description(f"Finished Checking {face_name}")
            facebar.refresh()
            counter = counter + 1            
        count_dup = len(duplicates)
        if count_dup > 0:
            cu.set_log_verbose(True)
            cu.log(f"Found {count_dup} duplicates names, check check_names.log file for futher detail.")
            quit()     


