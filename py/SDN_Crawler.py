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
    print('\nCrawling newest SDN_list')
    soup = bs(rq.get(url).text, 'html.parser')
    for i in soup.select('td'):
        title = []
        df = []
        for k in i.select('strong'):
            if k.text[2] != ')':
                title.append(k.text.replace(u'\xa0', '').strip())
        try:
            for j in title[:-1]:
                if j in title_list:
                    df.append(
                        i.text[
                            i.text.find(j)+len(j):
                                i.text.find(
                                    title[title.index(j)+1])
                        ].replace('\n', '').replace('\t', '').strip()
                    )
                else:
                    if 'QDi' in j:
                        df.append(j)
                    else:
                        df.append('')
            name_list = []
            for j in df[1].split(':'):
                name = ''.join(re.findall(r"\D", j)).strip()
                name = (name if name != 'na' else '')
                if name != '' or name is not None or name != '\n':
                    name_list.append(name)
            df[1] = '\n'.join(name_list[1:])
            if df != [] or df[0] != '':
                sql.insert_data('SDN', df)
        except:
            pass

def run(sql):
    request(sql, get_url())

