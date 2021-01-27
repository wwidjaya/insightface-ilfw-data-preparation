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
# 

import selenium
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER, logging
from selenium.webdriver.chrome.options import Options


from util import CommonUtil as cu
from util import ImageUtil as iu
from util import FaceUtil as fu
import time
import os
from urllib.request import Request, urlopen
import numpy as np
import cv2
from tqdm import tqdm

WINDOW_SIZE = "1920,1080"
GOOGLE_IMAGE_URL = 'https://images.google.com'
SEARCH_BOX_SELECTOR = 'input.gLFyf'
IMAGE_PATH = 'downloads'
SEARCH_URL = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"


class GoggleImageCrawler:
    def __init__(self, args):
        self.args = args
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=%s" % WINDOW_SIZE)
        self.options.add_argument("--log-level=%s" % 3)
        self.facebar = None
        self.imageBar = None


    def crawl(self, faces, callback):
        exec_path = self.args.chrome_exec_path
        self.wd = webdriver.Chrome(
            chrome_options=self.options, executable_path=exec_path)
        self.facebar = cu.get_primary_bar(faces)
        for face in self.facebar:
            iu.init_duplicate_check()
            self.wd.get(GOOGLE_IMAGE_URL)
            search_box = self.wd.find_element_by_css_selector(
                SEARCH_BOX_SELECTOR)
            search_box.send_keys(face)
            self.image_count = 0
            self.count = 0
            self.facebar.refresh()
            self.imageBar = cu.get_secondary_bar(bar_total=self.args.max_faces, bar_desc=f"Download image for {face}")
            self.fetch_image_urls(face, callback)
            self.imageBar.close()
        self.facebar.close()
        self.wd.quit()

    def url_to_image(self, url: str):
        t = cu.timing("Getting " + url)
        ext = cu.get_file_ext_from_url(url)
        image = iu.get_blank_image()
        try:
            req = Request(url)
            req.add_header(
                'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
            req.add_header(
                'Accept', 'image/*,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            req.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')
            req.add_header('Accept-Encoding', 'none')
            req.add_header('Accept-Language', 'en-US,en;q=0.8')
            req.add_header('Connection', 'keep-alive')
            t(", and done.")
            cu.log("Converting url {} to image", url)
            image = np.asarray(bytearray(urlopen(req).read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            cu.log("Finish converting url {} to image", url)
        except Exception as e:
            cu.log(f"Error while trying to get image from url {url} {e}")
        return image, ext

    def persist_image(self, folder_path: str, file_name: str, url: str, callback):
        try:
            image, ext = self.url_to_image(url)
            is_found, is_valid = iu.is_duplicate(image)
            if not is_valid:
                raise Exception("find invalid  image: {}".format(url))
            if is_found:
                raise Exception("find duplicate image: {}".format(url))

            if ext == "":
                ext = ".jpg"

            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            folder_path = os.path.join(folder_path, file_name)

            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            self.count = self.count + 1
            file_path = fu.get_full_file_name(
                folder_path, file_name, self.count, ext)

            cu.log("Writing image file {}", file_path)
            cv2.imwrite(file_path, image)
            cu.log("Finished Writing image file {}", file_path)
            result = 0
            try:
                result = callback(file_path, iu)
            except:
                # rollback the counter
                cu.remove_file(file_path)
                self.count = self.count - 1
                raise
            return result
        except Exception as e:
            cu.log(f"ERROR - Could not save {url} - {e}")
            raise

    def fetch_image_urls(self, query: str, callback):
        def scroll_to_end(wd):
            wd.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
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
            thumbnail_results = self.wd.find_elements_by_css_selector(
                "img.Q4LuWd")
            number_results = len(thumbnail_results)
            for img in thumbnail_results[results_start:number_results]:
                # try to click every thumbnail such that we can get the real image behind it
                try:
                    img.click()
                    time.sleep(sleep_between_interactions)
                except Exception:
                    continue

                # extract image urls
                actual_images = self.wd.find_elements_by_css_selector(
                    'img.n3VNCb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        try:
                            url = actual_image.get_attribute('src')
                            image_count = image_count + self.persist_image(
                                folder_path=images_path, file_name=fu.get_face_name(query), url=url, callback=callback)
                            image_urls.add(url)
                            self.imageBar.update(1)
                            self.imageBar.refresh()
                        except Exception as e:
                            cu.log(f"ERROR - Could not save {url} - {e}")

                if image_count >= max_image_count:
                    break
            else:
                time.sleep(30)
                return
                load_more_button = self.wd.find_element_by_css_selector(
                    ".mye4qd")
                if load_more_button:
                    wd.execute_script(
                        "document.querySelector('.mye4qd').click();")

            # move the result startpoint further down
            results_start = len(thumbnail_results)

        return image_urls
