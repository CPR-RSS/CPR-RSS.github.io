from urllib.request import urlopen

from bs4 import BeautifulSoup
import tqdm

from paper_parser import BasePaperListParser, Paper


class PaperListParser(BasePaperListParser):

    def __init__(self, args):
        self.base_url = "http://openaccess.thecvf.com/CVPR%s.py" % (args.year)
        self.website_url = "http://openaccess.thecvf.com/"

    def parse(self, html_soup):
        all_container = html_soup.select("dt.ptitle")
        paper_list = []
        overall = 0
        faild = 0
        for container in tqdm.tqdm(all_container):
            try:
                title = container.select('a')[0].get_text()
                url = container.select('a')[0].get('href')
                paper_list.append((title, url))
                overall += 1
            except:
                faild += 1
                # print("Paper [%s] does not have a related url" % title)
                pass
        print("Parse %s; Overall: %d, faild: %d " \
                % (self.base_url, overall, faild))
        return paper_list

    def cook_paper(self, paper_info):
        try:
            page_content = urlopen(self.website_url + paper_info[1]).read().decode('utf8')
            soup = BeautifulSoup(page_content, features="html.parser")
            author_list = soup.select('#authors >b >i')[0].get_text().split(',')
            author_list = [self.text_process(x) for x in author_list]
            abstract = self.text_process(soup.select('#abstract')[0].get_text())
            pdf_url = self.website_url +  next(filter(lambda x: 'pdf' in x.get_text(), soup.select('a'))).get('href')
            return Paper(self.text_process(paper_info[0]), abstract, pdf_url, author_list)
        except Exception as e:
            print(e)
            return (paper_info[0], e, self.base_url, [])
