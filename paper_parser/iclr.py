import re
from urllib.request import urlopen

from bs4 import BeautifulSoup
from paper_parser import Paper
from paper_parser.nips import PaperListParser

class PaperListParser(PaperListParser):
    def __init__(self, args):
        super().__init__(args)
        self.base_url = "https://iclr.cc/Conferences/%s/Schedule" % (args.year)


    def cook_paper(self, paper_info):
        try:
            page_content = urlopen(paper_info[1]).read().decode('utf8')
            soup = BeautifulSoup(page_content, features="html.parser")
            author_list = soup.select('div.meta_row > h3')[0].get_text().split(', ')
            author_list = [self.text_process(x) for x in author_list]
            abstract = self.text_process(soup.select('span.note-content-value')[0].get_text())
            pdf_url = paper_info[1]  # instead of return pdf link, we return the openreview page
            return Paper(self.text_process(paper_info[0]), abstract, pdf_url, author_list)
        except Exception as e:
            print(e)
            return (paper_info[0], e, self.base_url, [])