# -*- coding: utf-8 -*-
import sys
import requests
from collections import defaultdict

import tqdm
from bs4 import BeautifulSoup

from .base import BaseParser, Paper


class ECVAParser(BaseParser):

    def __init__(self, args):
        if args.conference.lower() == 'iccv':
            assert args.year % 2 == 1, "ICCV holds at odd years."
        self.re_format = "eccv_%d" % args.year
        self.website_url = "https://www.ecva.net/"
        self.base_url = "https://www.ecva.net/papers.php"

    def parse(self, html_soup, url=None):
        # import pdb; pdb.set_trace()
        all_container = html_soup.select("dt.ptitle")
        paper_list = []
        overall = 0
        failed = 0
        for container in tqdm.tqdm(all_container, '' if url is None else url):
            try:
                title = container.select('a')[0].get_text()
                url = container.select('a')[0].get('href')
                if self.re_format in url:
                    paper_list.append((title, url))
                    overall += 1
            except Exception as e:
                print("Line (%d): %s" % (sys._getframe().f_lineno, str(e)))
                failed += 1
                # print("Paper [%s] does not have a related url" % title)
                pass
        return paper_list, {'overall': overall, 'failed': failed}

    def cook_paper(self, paper_info):
        try:
            page_content = requests.get(self.website_url + paper_info[1]).content.decode('utf-8')
            soup = BeautifulSoup(page_content, features="html.parser")
            author_list = soup.select('#authors >b >i')[0].get_text().split(',')
            author_list = [self.text_process(x) for x in author_list]
            abstract = self.text_process(soup.select('#abstract')[0].get_text())
            pdf_url = '{}{}'.format(
                self.website_url,
                next(filter(lambda x: 'pdf' in x.get_text(), soup.select('a'))).get('href')
            )
            return Paper(self.text_process(paper_info[0]), abstract, pdf_url, author_list)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Line (%d): %s" % (sys._getframe().f_lineno, str(e)))
            return (paper_info[0], e, self.website_url, [])
