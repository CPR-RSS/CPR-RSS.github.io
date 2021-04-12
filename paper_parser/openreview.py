import sys
import requests
from collections import defaultdict
from soupsieve import select
from soupsieve.util import lower

import tqdm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from .base import BaseParser, Paper


def read_page(url, delay=30, signature='note'):
    if signature == 'note':
        print('reading page:{}; max timeout={}...'.format(url, delay))
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    try:
        _ = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, signature))
        )
    except Exception as e:
        print("Line (%d): %s" % (sys._getframe().f_lineno, str(e)))
    page = browser.page_source
    browser.close()
    return page


class OpenreviewParser(BaseParser):
    def __init__(self, args):
        super().__init__(args)
        self.category = ['poster', 'spotlight', 'talk']
        self.base_urls = [
            "https://openreview.net/group?id=ICLR.cc/{}/Conference#accept-{}".format(args.year, t)
            for t in self.category
        ]
        self.website_url = "https://openreview.net"

    def parse_paper_list(self, args):
        paper_list = []
        parse_log = defaultdict(lambda: 0)
        print("Found the following containers:")
        for url in self.base_urls:
            page_content = read_page(url)
            soup = BeautifulSoup(page_content, features="html.parser")
            lists, log = self.parse(soup, url)
            paper_list.extend(lists)
            parse_log = {key: parse_log[key] + log[key] for key in log}
        print("{url}, Overall: {overall}, failed: {failed} ".format(url=self.base_url, **parse_log))
        return paper_list

    def parse(self, html_soup, url=None):

        all_container = html_soup.select("li.note")
        paper_list = []
        overall = 0
        failed = 0
        for container in tqdm.tqdm(all_container, '' if url is None else url):
            try:
                title = container.select('h4 > a')[0].get_text().strip()
                url = container.select('h4 > a')[1].get('href')
                # import pdb; pdb.set_trace()
                author_list = [self.text_process(x.get_text())
                               for x in container.select('div.note-authors > a')
                               ]
                abstract = [item.select_one('.note-content-value').get_text()
                            for item in container.select('ul.note-content > li')
                            if 'abstract' in item.select_one('.note-content-field').get_text().lower()
                            ][0]
                paper_list.append((title, abstract, url, author_list))
                overall += 1
            except Exception as e:
                print("Line (%d): %s" % (sys._getframe().f_lineno, str(e)))
                failed += 1
                # print("Paper [%s] does not have a related url" % title)
                pass
        return paper_list, {'overall': overall, 'failed': failed}

    def cook_paper(self, paper_info):
        try:
            return Paper(self.text_process(paper_info[0]),
                         self.text_process(paper_info[1]),
                         self.website_url + paper_info[2],
                         paper_info[3])
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Line (%d): %s" % (sys._getframe().f_lineno, str(e)))
            return (paper_info[0], e, self.website_url + paper_info[1], [])
