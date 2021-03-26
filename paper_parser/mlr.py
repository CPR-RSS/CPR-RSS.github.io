import re
import sys
import requests
import tqdm

from bs4 import BeautifulSoup

from .base import BaseParser, Paper

SUFFIX = {
    'icml': {
        2018: "v80/",
        2019: "v97/",
        2020: "v119/",
    },
}


class MLRParser(BaseParser):
    def __init__(self, args):
        super().__init__(args)
        self.website_url = "http://proceedings.mlr.press/"
        self.base_url = self.website_url + SUFFIX[args.conference][args.year]

    def parse(self, html_soup):
        all_container = html_soup.select("div.paper")
        paper_list = []
        overall = 0
        failed = 0
        for container in tqdm.tqdm(all_container):
            overall += 1
            try:
                title = container.select('p.title')[0].get_text()
                url = container.select('p.links')[0].select("a")[0].get('href').strip('\n')
                # assert "PDF" in container.select('a.href_PDF')[0].get_text()
                paper_list.append((title, url))
            except Exception as e:
                print("Line (%d): %s" % (sys._getframe().f_lineno, str(e)))
                failed += 1
                pass
        return paper_list, {'overall': overall, 'failed': failed}

    def cook_paper(self, paper_info):
        try:
            # import pdb; pdb.set_trace()
            page_content = requests.get(paper_info[1]).content.decode('utf-8')
            soup = BeautifulSoup(page_content, features="html.parser")
            # author_list = re.split('\n+\s+', re.sub(',|;', '',
            #                        soup.select('.authors')[0].get_text()))[1:-1]
            author_list = soup.select('.authors')[0].get_text().split(',')
            author_list = [self.text_process(x) for x in author_list]
            abstract = self.text_process(soup.select('#abstract')[0].get_text())
            pdf_url = next(filter(lambda x: 'Download PDF' in x.get_text(),
                           soup.select('a'))).get('href')
            return Paper(self.text_process(paper_info[0]), abstract, pdf_url, author_list)
        except Exception as e:
            print(e)
            return (paper_info[0], e, self.base_url, [])
