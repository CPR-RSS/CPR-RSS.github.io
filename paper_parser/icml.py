import re
from urllib.request import urlopen

from bs4 import BeautifulSoup
from paper_parser import Paper
from paper_parser.nips import PaperListParser

class PaperListParser(PaperListParser):
    def __init__(self, args):
        super().__init__(args)
        self.website_url = "https://icml.cc"
        self.base_url = "https://icml.cc/Conferences/%s/Schedule" % (args.year)


    def cook_paper(self, paper_info):
        try:
            page_content = urlopen(paper_info[1]).read().decode('utf8')
            soup = BeautifulSoup(page_content, features="html.parser")
            author_list = re.split('\n+\s+', re.sub(',|;', '', soup.select('#authors')[0].get_text()))[1:-1]
            author_list = [self.text_process(x) for x in author_list]
            abstract = self.text_process(soup.select('#abstract')[0].get_text())
            pdf_url = next(filter(lambda x: 'Download PDF' in x.get_text(), soup.select('a'))).get('href')
            return Paper(self.text_process(paper_info[0]), abstract, pdf_url, author_list)
        except Exception as e:
            print(e)
            return (paper_info[0], e, self.base_url, [])