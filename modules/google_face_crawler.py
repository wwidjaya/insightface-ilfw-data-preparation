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





