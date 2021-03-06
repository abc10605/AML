import pathlib
import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Browser():
    def __init__(self):                                                         # 設定chromedriver路徑
        if platform.system() == "Windows":
            # AML/chromedriver
            self.__driver_path = f'{pathlib.Path(__file__).parent.parent}/chromedriver.exe'
        else:
            self.__driver_path = f'{pathlib.Path(__file__).parent.parent}/chromedriver'

    def open_browser(self):                                                     # 打開瀏覽器
        chrome_options = Options()
        # 無痕模式
        chrome_options.add_argument('--incognito')                              # 無痕模式
        self.__browser = webdriver.Chrome(
            executable_path=self.__driver_path,
            chrome_options=chrome_options
        )

    def search(self, url):                                                      # 前往網址
        self.__browser.get(url)

    def find_partial_link_text(self, *args):                                    # 查找帶有特定字的網頁元素
        for arg in args:
            WebDriverWait(self.__browser, 30, .5).until(                        # 等待直到特定元素出現
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, arg)))
            ActionChains(self.__browser).move_to_element(                       # 點擊元素
                self.__browser.find_element_by_partial_link_text(arg)
            ).click().perform()

    def switch_to_window(self, seq):                                            # 切換分頁
        self.__browser.switch_to.window(self.__browser.window_handles[seq])

    def close_browser(self):                                                    # 關閉瀏覽器
        self.__browser.quit()

    def get_url(self):                                                          # 取得現在分頁的網址
        return self.__browser.current_url
