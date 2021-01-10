import re

import requests as rq
from bs4 import BeautifulSoup as bs

from . import Browser


class SDN_Crawler():
    def __init__(self, sql):  # Constructor
        self.__title_list = tuple([
            'Name:',
            'Name (original script):',
            'Title:',
            'Designation:',
            'DOB:',
            'POB:',
            'Good quality a.k.a.:',
            'Low quality a.k.a.:',
            'Nationality:',
            'Passport no:',
            'National identification no:',
            'Address:',
            'Listed on:'
        ])
        self.__request(sql, self.__get_url())

    def __get_url(self):
        browser = Browser.Browser()
        browser.open_browser()
        browser.search('https://www.mjib.gov.tw/mlpc')
        browser.find_partial_link_text('號決議制裁名單')
        browser.switch_to_window(1)
        browser.find_partial_link_text('HTML')
        url = browser.get_url()
        browser.close_browser()
        return url

    def __request(self, sql, url):
        print('\nCrawling newest SDN_list')
        self.__soup = bs(rq.get(url).text, 'html.parser')
        for i in self.__soup.select('td'):
            self.__title = []
            self.__df = []
            for k in i.select('strong'):
                if k.text[2] != ')':
                    self.__title.append(k.text.replace(u'\xa0', '').strip())
            try:
                for j in self.__title[:-1]:
                    if j in self.__title_list:
                        self.__df.append(
                            i.text[
                                i.text.find(j)+len(j):
                                    i.text.find(
                                        self.__title[self.__title.index(j)+1])
                            ].replace('\n', '').replace('\t', '').strip()
                        )
                    else:
                        if 'QDi' in j:
                            self.__df.append(j)
                        else:
                            self.__df.append('')
                name_list = []
                for j in self.__df[1].split(':'):
                    name = ''.join(re.findall(r"\D", j)).strip()
                    name = (name if name != 'na' else '')
                    if name != '' or name is not None or name != '\n':
                        name_list.append(name)
                self.__df[1] = '\n'.join(name_list[1:])
                if self.__df != [] or self.__df[0] != '':
                    sql.insert_data('SDN', self.__df)
            except:
                pass
