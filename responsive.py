from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from math import ceil
from urllib.parse import urlparse
import re
import os
# Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--js-flags=--max-old-space-size=4096")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-logging")

class ResponsiveTester:

    def __init__(self, urls):
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.browser.maximize_window()
        self.urls = urls
        self.sizes = [480,960,1366,1920]
        self.BROWSER_HEIGHT = 1007

    def screenshot(self,url,dir):
        self.browser.get(url)
        for size in self.sizes:
            self.browser.set_window_size(size, self.BROWSER_HEIGHT)
            self.browser.execute_script("window.scrollTo(0,0)")
            time.sleep(3)

            # 네비게이션 바의 높이를 고려하여 스크롤 값 계산
            nav_bar_height = 64
            inner_height = self.browser.execute_script("return window.innerHeight") - nav_bar_height
            
            scroll_size = self.browser.execute_script("return document.body.scrollHeight")
            total_sections = ceil(scroll_size / inner_height)

            for section in range(total_sections+1):
                self.browser.execute_script(f"window.scrollTo(0,{(section) * inner_height})")
                self.browser.save_screenshot(f"screenshots/{dir}/{dir}_{size}p_{section}.png")
                time.sleep(3)

    def start(self):
        for url in self.urls:
            parsed = urlparse(url).netloc.replace("www.", "")
            dir = re.sub(r'\.\w*', "", parsed)
            check_path = os.path.isdir(f'./screenshots/{dir}')
            if not check_path:
                os.mkdir(f'./screenshots/{dir}')
            else:
                pass
            self.screenshot(url, dir)

            

        
tester = ResponsiveTester(["https://duckat.kr/"])
tester.start()








