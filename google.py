from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait



# Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--js-flags=--max-old-space-size=4096")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-logging")


class GoogleKeywordScreenshooter():
        
        def __init__(self, keyword,screenshots_dir):
            self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            self.keyword = keyword
            self.screenshots_dir = screenshots_dir
        
     
        def start(self):
            self.browser.get("https://google.com")
            search_bar = self.browser.find_element(By.CLASS_NAME, "gLFyf")
            search_bar.send_keys(self.keyword)
            search_bar.send_keys(Keys.ENTER)
            try:
                shitty_elements = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cUnQKe, .ULSxyf"))
                )
                for shitty in shitty_elements:
                    self.browser.execute_script(
                        """
                        const shitty = arguments[0];
                        shitty.parentNode.removeChild(shitty);
                        """,
                        shitty
                    )
            except Exception:
                 pass
            
            search_results = WebDriverWait(self.browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "MjjYud")))
            for index, search_result in enumerate(search_results):
                print(f"Processing search result {index}")
                search_result.screenshot(f"{self.screenshots_dir}/{self.keyword}x{index}.png")

        def finish(self):
             self.browser.quit()



domain_competitors = GoogleKeywordScreenshooter("buy domain", "screenshots")
domain_competitors.start()
domain_competitors.finish()
python_competitors = GoogleKeywordScreenshooter("python book", "screenshots")
python_competitors.start()
python_competitors.finish()

