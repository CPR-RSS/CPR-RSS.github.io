# -*- coding: utf-8 -*-
import re
import requests
from collections import namedtuple


from bs4 import BeautifulSoup


class BaseParser:
    """
    """
    def __init__(self, url):
        self.base_url = None
    
    def parse(self, soup):
        raise NotImplementedError()

    def parse_paper_list(self, args):
        base_url = self.base_url
        print(base_url)
        content = requests.get(base_url).text
        soup = BeautifulSoup(content, features="html.parser")
        paper_list, parse_log = self.parse(soup)
        print("{url}, Overall: {overall}, failed: {failed} ".format(url=self.base_url, **parse_log))
        return paper_list

    @staticmethod
    def text_process(text):
        text = text.replace('&', "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace('>', "&gt;")
        text = text.replace("'", "&apos;")
        text = text.replace('"', "&quot;")
        text = text.replace("’", "'")
        # re.sub(u"[\x01-\x1f|\x22|\x26|\x27|\x2f|\x3c|\x3e]+",u"",sourceString)
        # text = text.replace("{", '(')
        # text = text.replace('}', ')')
        text = re.sub('[^!-~]+', ' ', text).strip()
        # text = text.replace('', ' ')
        # text = text.replace('', ' ')
        # text = text.replace('', ' ')
        # text = text.replace('', ' ')
        # text = text.replace('', ' ')
        # text = text.replace('', ' ')
        # text = text.replace('', ' ')
        # text = text.replace('', ' ')
        # text = text.replace('', ' ')
        # text = text.replace('', ' ')
        return text


Paper = namedtuple('Paper', ['title', 'abstract', 'pdf_url', 'author_list'])
