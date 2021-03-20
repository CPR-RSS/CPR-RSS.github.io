from urllib.request import urlopen

from bs4 import BeautifulSoup
import tqdm

from paper_parser import BasePaperListParser, Paper


class PaperListParser(BasePaperListParser):

    def __init__(self, args):
        self.base_url = "https://nips.cc/Conferences/%s/Schedule" % (args.year)
        self.website_url = "http://papers.nips.cc"

    def parse(self, html_soup):
        all_container = html_soup.select("div.maincard")
        paper_list = []
        spotlight = 0
        oral = 0
        poster = 0
        overall = 0
        faild = 0
        for container in tqdm.tqdm(all_container):
            suffix = ""
            if "Spotlight" in container.get('class'):
                suffix = " (Spotlight)"
                spotlight += 1
            elif "Oral" in container.get('class'):
                suffix = ' (Oral)'
                oral += 1
            elif "Poster" in container.get('class'):
                poster += 1
            else:
                continue
            overall += 1
            try:
                title = container.select('div.maincardBody')[0].get_text() + suffix
                url = container.select('a.href_PDF')[0].get('href')
                # assert "PDF" in container.select('a.href_PDF')[0].get_text()
                paper_list.append((title, url))
            except Exception as e:
                print(e)
                faild += 1
                # print("Paper [%s] does not have a related url" % title)
                pass
        print("Parse %s; spotlight: %d, Oral: %d, Poster: %d, Overall: %d, faild: %d " \
                % (self.base_url, spotlight, oral, poster, overall, faild))
        return paper_list

    def cook_paper(self, paper_info):
        try:
            page_content = urlopen(paper_info[1]).read().decode('utf8')
            soup = BeautifulSoup(page_content, features="html.parser")
            author_list = [self.text_process(x.get_text()) for x in soup.select('li.author')]
            abstract = self.text_process(soup.select('p.abstract')[0].get_text())
            pdf_url = self.website_url + next(filter(lambda x: '[PDF]' in x.get_text(), soup.select('a'))).get('href')
            return Paper(self.text_process(paper_info[0]), abstract, pdf_url, author_list)
        except Exception as e:
            print(e)
            return (paper_info[0], e, self.base_url, [])
