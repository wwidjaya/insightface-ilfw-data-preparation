import os
import random
import argparse


class PairGenerator:
    def __init__(self, data_dir, pairs_filepath, img_ext):
        """
        Parameter data_dir, is your data directory.
        Parameter pairs_filepath, where is the pairs.txt that belongs to.
        Parameter img_ext, is the image data extension for all of your image data.
        """
        self.data_dir = data_dir
        self.pairs_filepath = pairs_filepath
        self.img_ext = img_ext

    # splitting the database content into 10 random sets
    def split_to_10(self):
        folders = []
        cnt = 0
        for name in os.listdir(self.data_dir):
            folders.append(name)
        folders = sorted(folders) # sorting names in abc order

        a = []
        # names of folders - e.g. Talgat Bigeldinov, Kairat Nurtas, etc.
        for name in folders:             
            # f = open(self.pairs_filepath, 'a+')
            # looping through image files in one folder 
            for file in os.listdir(self.data_dir + '/' + name):
                # a.append(data_dir + name + '/' + file)

                a.append(name)
                cnt = cnt + 1
            cnt = cnt + 1            
        random.shuffle(a)


    # splitting the database content into 10 random sets

    def write_similar(self, lst):
        f = open(self.pairs_filepath, 'a+')
        for i in range(20):
            left = random.choice(lst)
            right = random.choice(lst)
            f.write(left + '\t' + right + '\t' + '1\n')

    # writing 1 IMAGE_PATH LABEL like insightface lst file needs
    def write_item_label(self):
        cnt = 1
        for name in os.listdir(self.data_dir):
            if name == ".DS_Store":
                continue
            # print(name)
            a = []
            f = open(self.pairs_filepath, 'a+')
            for file in os.listdir(self.data_dir + '/' + name):
                if file == ".DS_Store":
                    continue
                a.append(self.data_dir + '/' + name + '/' + file)
                f.write(str(1) + '\t' + data_dir + '/' + name + '/' + file + '\t' + str(cnt) + '\n')
            cnt = cnt + 1

    # writing 1 IMAGE_PATH LABEL like insightface lst file needs in alphabetic order
    def write_item_label_abc(self):
        cnt = 1
        names = []
        for name in os.listdir(self.data_dir):
            names.append(name)

        names = sorted(names)

        for name in names:
            print(name)
            a = []
            f = open(self.pairs_filepath, 'a+')
            for file in os.listdir(self.data_dir + '/' + name):
                if file == ".DS_Store":
                    continue
                a.append(self.data_dir + '/' + name + '/' + file)
                f.write(str(1) + '\t' + self.data_dir + '/' + name + '/' + file + '\t' + str(cnt) + '\n')
            cnt = cnt + 1

    def write_different(self, lst1, lst2):
        f = open(self.pairs_filepath, 'a+')
        for i in range(500):
            left = random.choice(lst1)
            right = random.choice(lst2)
            f.write(left + '\t' + right + '\t' + '0\n')
        f.close()

    def generate_pairs(self):
        for name in os.listdir(self.data_dir):
            if name == ".DS_Store":
                continue

            a = []
            for file in os.listdir(self.data_dir + '/' + name):
                if file == ".DS_Store":
                    continue
                a.append(name + '/' + file)

            self.write_similar(a)

    def generate_non_pairs(self):
        folder_list = []
        for folder in os.listdir(self.data_dir):
            folder_list.append(folder)
        folder_list.sort(reverse=True)
        # print(folder_list)
        i = 0
        a = []
        for dir in os.listdir(self.data_dir):
            if dir == ".DS_Store":
                continue

            for file in os.listdir(self.data_dir + dir):
                if file == ".DS_Store":
                    continue
                a.append(dir + '/' + file)
            # print(a)
        b = []
        for dir in os.listdir(self.data_dir):
            if dir == ".DS_Store":
                continue

            for file in os.listdir(self.data_dir + folder_list[i]):
                if file == ".DS_Store":
                    continue
                b.append(folder_list[i] + '/' + file)
            # print(b)
            i = i + 1

        self.write_different(a, b)


