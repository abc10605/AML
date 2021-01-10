import pathlib
import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Browser():
    def __init__(self):
        if platform.system() == "Windows":
            self.__driver_path = f'{pathlib.Path(__file__).parent.parent}/chromedriver.exe'
        else:
            self.__driver_path = f'{pathlib.Path(__file__).parent.parent}/chromedriver'

    def open_browser(self):
        chrome_options = Options()
        chrome_options.add_argument('--incognito')
        self.__browser = webdriver.Chrome(
            executable_path=self.__driver_path,
            chrome_options=chrome_options
        )

    def search(self, url):
        self.__browser.get(url)

    def find_partial_link_text(self, *args):
        for arg in args:
            WebDriverWait(self.__browser, 30, .5).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, arg)))
            ActionChains(self.__browser).move_to_element(
                self.__browser.find_element_by_partial_link_text(arg)
            ).click().perform()

    def switch_to_window(self, seq):
        self.__browser.switch_to.window(self.__browser.window_handles[seq])

    def close_browser(self):
        self.__browser.quit()

    def get_url(self):
        return self.__browser.current_url
