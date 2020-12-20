from  settings import faces
import argparse
from google_face_crawler import GoogleFaceCrawler 

parser = argparse.ArgumentParser(description='Data Preparation Program for Face Recognition Thesis Project')
# general
parser.add_argument('--silent', default='True', help='Show crawler browser window')
parser.add_argument('--model-prefix', default='./models/model-r50-am-lfw/model', help='The model location prefix ')
parser.add_argument('--model-epoch', default=0, type=int, help='The model epoch')
parser.add_argument('--max-faces', default=100,  type=int, help='Maximum number of faces')
parser.add_argument('--image-size', default='112,112', help='The face image size')
parser.add_argument('--image-path', default='downloads', help='The image download paths')
parser.add_argument('--sleep', default=1,  type=int, help='Sleep between interaction')
parser.add_argument('--model', default='./models/model-r50-am-lfw/model,0', help='path to load model.')
parser.add_argument('--gpu', default=-1, type=int, help='GPU ID')
args = parser.parse_args()

if __name__ == '__main__':  
  gfc = GoogleFaceCrawler(args)
  gfc.crawl(faces)

