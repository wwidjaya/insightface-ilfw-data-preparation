import time
import datetime
from urllib.parse import urlparse
import os

class Common():

  def __init__(self):
    None
  
  def log(self, string:str, *args):
    print("{}:{}".format(datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"), string.format(*args)))

  def timing(self, action):
      start_time = time.time()
      self.log("Starting {}", action)
      return lambda x: self.log("[{:.2f}s] {} finished{}", time.time() - start_time, action, x)

  def get_file_ext_from_url(self, url:str):
    p = urlparse(url)
    return os.path.splitext(p.path)[1]

  def read_file_as_array(self, filename):
    lines = []
    with open(filename) as fp:
        for line in fp:
            lines.append(line.strip()) 
    return lines   

    
      

