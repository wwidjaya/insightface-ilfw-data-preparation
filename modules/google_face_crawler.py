import insightface
import selenium 
from selenium import webdriver 
import time
import requests
import os
from PIL import Image
import io
import cv2
import urllib
from  urllib.request import Request, urlopen 
import numpy as np
from  common import Common
from face_model import FaceModel
import hashlib
from selenium.webdriver.chrome.options import Options
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
        self.c = Common()
        t = self.c.timing("Initiating model")
        args.ctx_id = args.gpu
        self.model = FaceModel(args)
        t("")
    
    
    def process_image(self, file_path):
        self.c.log("processing image {}", file_path)
        ext = os.path.splitext(file_path)[1]
        face = cv2.imread(file_path)
        #faces = self.model.detect_faces(image=face, align_face=False)
        aligned_face = self.model.align_face(face)
        cv2.imwrite(file_path, aligned_face)
        #cv2.imwrite(file_path + '_ori' + ext, faces[0])
        return 1
    
    def crawl(self, faces):
        self.crawler.crawl(faces, self.process_image)





