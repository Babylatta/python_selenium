import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from decouple import config
from selenium.webdriver.common.action_chains import ActionChains


# Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--js-flags=--max-old-space-size=4096")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-logging")


class Instaminer : 
    def __init__(self, main_hashtag):
        self.main_hashtag = main_hashtag
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.extracted_hashtags = []

    def wait_for(self, locator):
        return WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(locator))
    
    def clean_hashtag(self, hashtag):
        return hashtag[1:]
    
    def save_file(self):
        file = open(f"{self.main_hashtag}_report.csv","w")
        writer = csv.writer(file)
        writer.writerow(["Hashtag", "Post Count"])

        for hashtag in self.extracted_hashtags:
            writer.writerow(hashtag)

    def start(self):
        INSTAGRAM_ID = config('ID')
        INSTAGRAM_PASSWORD = config('PW')

        self.browser.get("https://www.instagram.com/accounts/login/")

        self.wait_for(((By.CLASS_NAME, "_ab1y")))

        insta_id = self.wait_for(((By.NAME, "username")))
        insta_password = self.wait_for(((By.NAME, "password")))

        insta_id.send_keys(INSTAGRAM_ID)
        insta_password.send_keys(INSTAGRAM_PASSWORD)
        insta_password.send_keys(Keys.ENTER)

        not_now = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "_a9--._ap36._a9_1")))
        not_now.click()
        self.extract_data()
    
    def extract_data(self):
        self.main_hashtag = "#"+self.main_hashtag
        
        search = self.wait_for(((By.CSS_SELECTOR, 'svg[aria-label="Search"]')))
        search.click()

        search_bar = self.wait_for(((By.CSS_SELECTOR, '[aria-label="Search input"]')))
        search_bar.send_keys(self.main_hashtag)
        time.sleep(3)

        hashtag_box = self.wait_for(((By.CLASS_NAME,"xocp1fn")))
        hashtag_links = WebDriverWait(hashtag_box, 10).until(EC.presence_of_all_elements_located(((By.TAG_NAME, "a"))))


        for hashtag in hashtag_links:
            hashtag_name = hashtag.find_element(By.CLASS_NAME, "xuxw1ft")
            post_count = hashtag.find_element(By.CLASS_NAME, "html-span")

            if post_count:
                post_count = int(post_count.text.replace(",", ""))

            if hashtag_name:
                hashtag_name = self.clean_hashtag(hashtag_name.text)

            if hashtag_name and post_count:
                self.extracted_hashtags.append((hashtag_name, post_count))

        
        self.save_file()
        self.browser.quit()

Instaminer("cat").start()

