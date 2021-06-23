# -*- coding: utf-8 -*-
import sys
import requests
from collections import defaultdict

import tqdm
from bs4 import BeautifulSoup

from .base import BaseParser, Paper


class CVFParser(BaseParser):

    def __init__(self, args):
        if args.conference.lower() == 'iccv':
            assert args.year % 2 == 1, "ICCV holds at odd years."
        self.base_url = "http://openaccess.thecvf.com/%s%d" % (args.conference.upper(), args.year)
        self.website_url = "http://openaccess.thecvf.com/"

    def parse_paper_list(self, args):
        base_url = self.base_url
        if args.year < 2018:  # before 2018, those pages are organized locally
            return super().parse_paper_list(args)

        print("Parsing:" + base_url)
        _content = requests.get(base_url).content.decode('utf-8')
        found_urls = [self.website_url + dda.get('href')
                      for dda in BeautifulSoup(_content, features='html.parser').select("dd >a")]
        contents = [requests.get(url).content.decode('utf-8') for url in found_urls]
        paper_list = []
        parse_log = defaultdict(lambda: 0)
        found_all_container = sum(['all' in found_url.lower() for found_url in found_urls])
        if found_all_container:
            found_urls = found_urls[:-1]
            contents = contents[:-1]
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

    def cook_paper(self, paper_info):
        try:
            page_content = requests.get(self.website_url + paper_info[1]).content.decode('utf-8')
            soup = BeautifulSoup(page_content, features="html.parser")
            author_list = soup.select('#authors >b >i')[0].get_text().split(',')
            author_list = [self.text_process(x) for x in author_list]
            abstract = self.text_process(soup.select('#abstract')[0].get_text())
            pdf_url = '%s%s'.format(
                self.website_url,
                next(filter(lambda x: 'pdf' in x.get_text(), soup.select('a'))).get('href')
            )
            return Paper(self.text_process(paper_info[0]), abstract, pdf_url, author_list)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Line (%d): %s" % (sys._getframe().f_lineno, str(e)))
            return (paper_info[0], e, self.base_url, [])
