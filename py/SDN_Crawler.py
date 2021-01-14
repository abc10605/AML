import re

import requests as rq
from bs4 import BeautifulSoup as bs

from . import Browser


def get_url():
    browser = Browser.Browser()
    browser.open_browser()
    browser.search('https://www.mjib.gov.tw/mlpc')
    browser.find_partial_link_text('號決議制裁名單')
    browser.switch_to_window(1)
    browser.find_partial_link_text('HTML')
    url = browser.get_url()
    browser.close_browser()
    return url

def request(sql, url):                        
    title_list = tuple([
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
    print('\nCrawling newest SDN_list...', end='')
    soup = bs(rq.get(url).text, 'html.parser')
    for i in soup.select('td'):
        title = []
        df = []
        # 先抓內容的標題
        for j in i.select('strong'):
            if j.text[2] != ')':
                title.append(j.text.replace(u'\xa0', '').strip())
        if title != []:
            # 先append編號(ex. Qdi.XXX)
            df.append(title[0])
            # 迴圈13次
            for t in range(len(title_list)):
                # 無論內容如何，至少都會append None，確保欄位數量都是13
                try:
                    if title[t+1] in title_list:
                        SDN_title = title[t+1]
                        df.append(
                            i.text[
                                i.text.find(SDN_title)+len(SDN_title):
                                    i.text.find(
                                        title[title.index(SDN_title)+1])
                            ].replace('\n', '').replace('\t', '').strip()
                        )
                    else:
                        df.append(None)
                except:
                    df.append(None)
            # 處理人名
            name_list = []
            for j in df[1].split(':'):
                name = ''.join(re.findall(r"\D", j)).strip()
                name = (name if name != 'na' else None)
                if name != '' or name is not None or name != '\n':
                    name_list.append(name)
            try:
                if name_list[0] == '' or name_list[0] == '\n':
                    df[1] = '\n'.join(name_list[1:])
                else:
                    df[1] = '\n'.join(name_list)
            except:
                df[1] = None
            sql.insert_data('SDN', df)

def run(sql):
    request(sql, get_url())
    print('\rCrawling newest SDN_list...\033[33mFinished!\033[0m', flush=True)
