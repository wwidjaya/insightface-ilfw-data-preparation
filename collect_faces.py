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


from  settings import faces
import argparse
from google_face_crawler import GoogleFaceCrawler 

parser = argparse.ArgumentParser(description='Data Collection Program for Face Recognition Thesis Project')
# general
parser.add_argument('--silent', default='True', help='Show crawler browser window')
parser.add_argument('--model-prefix', default='./models/model-r50-am-lfw/model', help='The model location prefix ')
parser.add_argument('--model-epoch', default=0, type=int, help='The model epoch')
parser.add_argument('--max-faces', default=100,  type=int, help='Maximum number of faces')
parser.add_argument('--image-size', default='112,112', help='The face image size')
parser.add_argument('--image-path', default='downloads', help='The image download paths')
parser.add_argument('--image-format', default='.jpg', help='The image download paths')
parser.add_argument('--sleep', default=1,  type=int, help='Sleep between interaction')
parser.add_argument('--model', default='./models/model-r50-am-lfw/model,0', help='path to load model.')
parser.add_argument('--gpu', default=-1, type=int, help='GPU ID')
parser.add_argument('--chrome-exec-path', default='./modules/chromedriver.exe', help='path to load model.')
args = parser.parse_args()

if __name__ == '__main__':  
  gfc = GoogleFaceCrawler(args)
  gfc.crawl(faces)

