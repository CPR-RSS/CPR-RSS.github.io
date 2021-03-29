import sys
import requests
from collections import defaultdict

from bs4 import BeautifulSoup
from .base import BaseParser, Paper

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def read_page(url, delay=30):
    print('reading page:{}; max timeout={}...'.format(url, delay))
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    try:
        _ = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'note'))
        )
    except Exception as e:
        print("Line (%d): %s" % (sys._getframe().f_lineno, str(e)))
    print('loading {} papers'.format(len(browser.find_elements_by_class_name('note'))))
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
        base_url = self.base_urls[0]
        if args.year < 2018:  # before 2018, those pages are organized locally
            return super().parse_paper_list(args)

        print("Parsing:" + base_url)
        _content = read_page(base_url)
        import pdb; pdb.set_trace()
        found_urls = [self.website_url + dda.get('href')
                      for dda in BeautifulSoup(_content, features='html.parser').select("dd >a")]
        contents = [requests.get(url).content.decode('utf-8') for url in found_urls]
        paper_list = []
        parse_log = defaultdict(lambda: 0)
        print("Found the following containers:")
        for url, content in zip(found_urls, contents):
            soup = BeautifulSoup(content, features="html.parser")
            lists, log = self.parse(soup, url)
            paper_list.extend(lists)
            parse_log = {key: parse_log[key] + log[key] for key in log}
        print("{url}, Overall: {overall}, failed: {failed} ".format(url=self.base_url, **parse_log))
        return paper_list

    def parse(self, html_soup, url=None):
        all_container = html_soup.select("dt.ptitle")
        paper_list = []
        overall = 0
        failed = 0
        for container in tqdm.tqdm(all_container, '' if url is None else url):
            try:
                title = container.select('a')[0].get_text()
                url = container.select('a')[0].get('href')
                paper_list.append((title, url))
                overall += 1
            except Exception as e:
                print("Line (%d): %s" % (sys._getframe().f_lineno, str(e)))
                failed += 1
                # print("Paper [%s] does not have a related url" % title)
                pass
        return paper_list, {'overall': overall, 'failed': failed}


# class PaperListParserCC(PaperListParser):
#     def __init__(self, args):
#         super().__init__(args)
#         self.base_url = "https://iclr.cc/Conferences/%s/Schedule" % (args.year)

#     def cook_paper(self, paper_info):
#         try:
#             page_content = urlopen(paper_info[1]).read().decode('utf8')
#             soup = BeautifulSoup(page_content, features="html.parser")
#             author_list = soup.select('div.meta_row > h3')[0].get_text().split(', ')
#             author_list = [self.text_process(x) for x in author_list]
#             abstract = self.text_process(soup.select('span.note-content-value')[0].get_text())
#             pdf_url = paper_info[1]  # instead of return pdf link, we return the openreview page
#             return Paper(self.text_process(paper_info[0]), abstract, pdf_url, author_list)
#         except Exception as e:
#             print(e)
#             return (paper_info[0], e, self.base_url, [])


# from paper_parser import BasePaperListParser, Paper
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
# from tqdm import tqdm





# class PaperListParserOPEN(BasePaperListParser):
#     def __init__(self, args):
#         ts=['poster','spotlight','talk']
#         self.base_urls = ["https://openreview.net/group?id=ICLR.cc/{}/Conference#accept-{}".format(args.year,t) for t in ts]
#         self.website_url = "https://openreview.net"
    
#     def getinfo(self,d):
#         author=d.select('div.note-authors')[0].get_text().strip()
#         title=d.select('h4')[0].get_text().strip()
#         details=d.select('ul[class="list-unstyled note-content"]')[0].select('li')
#         for x in details:
#             if x.strong.text=='Abstract:':
#                 abstract=x.span.get_text()
#             if x.strong.text=='Original Pdf:':
#                 pdf=x.span.a['href']

#         return title,abstract,pdf,author
   
#     def parse_paper_list(self, args):
#         paper_list=[]
#         for url in self.base_urls:
#             page=read_page(url)
#             paper_list.extend(self.parse(BeautifulSoup(page,features="html.parser")))
#         return paper_list
    
#     def parse(self, soup):
#         table_contents=soup.select('.tab-content')[0].select('div[class="tab-pane fade active in"]')
#         lis=table_contents[0].select('li.note')
#         paper_list=[]
#         succ=0
#         fail=0
#         with tqdm(lis) as t:
#             for li in t:
#                 try:
#                     info=self.getinfo(li)
#                     paper_list.append(info)
#                     succ+=1  
#                 except Exception as e:
#                     fail+=1
#                     print(e)
#                 t.set_postfix(succ=succ,fail=fail)
#         return paper_list

#     def cook_paper(self, paper_info):
#         title,abstract,pdf,author=paper_info
#         title=self.text_process(title)
#         author_list = [self.text_process(x) for x in author.split(',')]
#         abstract = self.text_process(abstract)
#         pdf_url = self.website_url + self.text_process(pdf)
#         return Paper(title,abstract,pdf_url,author_list)