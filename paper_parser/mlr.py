import re
from urllib.request import urlopen
import tqdm
from bs4 import BeautifulSoup
from paper_parser import Paper
from paper_parser import BasePaperListParser


class PaperListParser(BasePaperListParser):
    def __init__(self, args):
        super().__init__(args)
        self.website_url = "http://proceedings.mlr.press/"
        year_to_suffix = {
            2018: "v80/",
            2019: "v97/"
        }
        self.base_url = self.website_url + year_to_suffix[args.year]

    def parse(self, html_soup):
        all_container = html_soup.select("div.paper")
        paper_list = []
        overall = 0
        faild = 0
        for container in tqdm.tqdm(all_container):
            overall += 1
            try:
                title = container.select('p.title')[0].get_text()
                url = container.select('p.links')[0].select("a")[0].get('href')
                # assert "PDF" in container.select('a.href_PDF')[0].get_text()
                paper_list.append((title, url))
            except Exception as e:
                print(e)
                faild += 1
                # print("Paper [%s] does not have a related url" % title)
                pass
        print("Parse %d papers from %s, %d failed" % (overall, self.base_url,  faild))
        return paper_list

    def cook_paper(self, paper_info):
        try:
            page_content = urlopen(paper_info[1]).read().decode('utf8')
            soup = BeautifulSoup(page_content, features="html.parser")
            author_list = re.split('\n+\s+', re.sub(',|;', '',
                                   soup.select('#authors')[0].get_text()))[1:-1]
            author_list = [self.text_process(x) for x in author_list]
            abstract = self.text_process(soup.select('#abstract')[0].get_text())
            pdf_url = next(filter(lambda x: 'Download PDF' in x.get_text(),
                           soup.select('a'))).get('href')
            return Paper(self.text_process(paper_info[0]), abstract, pdf_url, author_list)
        except Exception as e:
            print(e)
            return (paper_info[0], e, self.base_url, [])
