import selenium 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from common import Common
import time
import os
from  urllib.request import Request, urlopen 
import numpy as np
import cv2

WINDOW_SIZE = "1920,1080"
GOOGLE_IMAGE_URL = 'https://images.google.com'
SEARCH_BOX_SELECTOR = 'input.gLFyf'
IMAGE_PATH = 'downloads'
SEARCH_URL = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
EXEC_PATH = "./modules/chromedriver.exe"

class GoggleImageCrawler:
  def __init__(self, args):  
    self.args = args
    self.c = Common()
    self.options = Options()
    self.options.add_argument("--headless")
    self.options.add_argument("--window-size=%s" % WINDOW_SIZE)

  def crawl(self, faces, callback):
    self.wd = webdriver.Chrome(chrome_options=self.options, executable_path=EXEC_PATH)
    for face in faces:
      self.wd.get(GOOGLE_IMAGE_URL)
      search_box = self.wd.find_element_by_css_selector(SEARCH_BOX_SELECTOR)
      search_box.send_keys(face)
      self.image_count = 0      
      self.count = 0
      self.fetch_image_urls(face, callback)
    self.wd.quit()


  def url_to_image(self, url:str):
      t = self.c.timing("Getting " + url)
      ext = self.c.get_file_ext_from_url(url)
      req = Request(url)
      req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
      req.add_header('Accept', 'image/*,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
      req.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')
      req.add_header('Accept-Encoding', 'none')
      req.add_header('Accept-Language', 'en-US,en;q=0.8')
      req.add_header('Connection', 'keep-alive')
      t(", and done.")
      image = np.asarray(bytearray(urlopen(req).read()), dtype="uint8")
      image = cv2.imdecode(image, cv2.IMREAD_COLOR)
      return image, ext


  def persist_image(self, folder_path:str, file_name:str, url:str, callback):
    try:
      image, ext = self.url_to_image(url)
      if ext == "":
          ext = ".jpg"
      thresh=0.5
      scale=1.0

      if not os.path.exists(folder_path):
          os.mkdir(folder_path)

      folder_path = os.path.join(folder_path, file_name)

      if not os.path.exists(folder_path):
          os.mkdir(folder_path)

      self.count = self.count + 1
      file_path = os.path.join(folder_path, file_name + "_" + str(self.count).zfill(4) + ext)
      cv2.imwrite(file_path, image)
      return callback(file_path)
    except Exception as e:
        self.c.log(f"ERROR - Could not save {url} - {e}")
        raise

  
  def fetch_image_urls(self, query:str, callback):    
    def scroll_to_end(wd):
      wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(sleep_between_interactions)    
  
    # load the page
    self.wd.get(SEARCH_URL.format(q=query))

    max_image_count = self.args.max_images
    sleep_between_interactions = self.args.sleep
    images_path = self.args.image_path

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_image_count:
        scroll_to_end(self.wd)
        # get all image thumbnail results
        thumbnail_results = self.wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        #print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = self.wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    try:
                        url=actual_image.get_attribute('src')
                        image_count = image_count + self.persist_image(folder_path=images_path, file_name=query.replace(" ", "_"), url=url, callback=callback)                        
                        image_urls.add(url)
                    except Exception as e:
                        self.c.log(f"ERROR - Could not save {url} - {e}")


            if image_count >= max_image_count:
                break
        else:
            time.sleep(30)
            return
            load_more_button = self.wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls
