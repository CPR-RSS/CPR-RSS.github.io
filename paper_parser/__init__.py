from __future__ import print_function

from collections import namedtuple

from urllib.request import urlopen
from bs4 import BeautifulSoup


class BasePaperListParser(object):
    """
    """
    def __init__(self, url):
        self.base_url = None
    
    def parse(self, soup):
        raise NotImplementedError()

    def parse_paper_list(self, args):
        base_url = self.base_url
        print(base_url)        
        content = urlopen(base_url).read()
        soup = BeautifulSoup(content, features="html.parser")
        paper_list = self.parse(soup)
        return paper_list

    @staticmethod
    def text_process(text):
        text = text.replace('&', "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace('>', "&gt;")
        text = text.replace("'", "&apos;")
        text = text.replace('"', "&quot;")
        text = text.replace('', '[UNKNOWN]')
        text = text.replace("’", "'")
        return text

Paper = namedtuple('Paper', ['title', 'abstract', 'pdf_url', 'author_list'])
