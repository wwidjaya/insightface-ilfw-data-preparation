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
import cv2
from  util import CommonUtil as cu
from face_model import FaceModel
from google_image_crawler import GoggleImageCrawler

class GoogleFaceCrawler:
    """
        Google Face Crawler
        v1.0
    """
    def __init__(self, args):
        # Copy arguments for Google Image Crawler
        args.max_images = args.max_faces
        self.crawler = GoggleImageCrawler(args)
        t = cu.timing("Initiating model")
        args.ctx_id = args.gpu
        self.model = FaceModel(args, use_large_detector=False)
        t("")
    
    
    def process_image(self, file_path, iu):
        cu.log("processing image {}", file_path)
        face = cv2.imread(file_path)
        cu.log("Aigning face {}", file_path)
        aligned_face = self.model.align_face(face)
        if iu.is_duplicate(aligned_face):
            raise Exception("Duplicate face found {}".format(file_path))
        cu.log("Writing aligned face {}", file_path)
        cv2.imwrite(file_path, aligned_face)
        cu.log("Finish Writing aligned face {}", file_path)
        return 1
    
    def crawl(self, faces):
        self.crawler.crawl(faces, self.process_image)





