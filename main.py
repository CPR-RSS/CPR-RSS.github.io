from __future__ import print_function

import importlib
from urllib.request import urlopen
import tqdm
from bs4 import BeautifulSoup

def parse_paper_list(parser, args):

    base_url = parser.base_url
    content = urlopen(base_url).read().decode('utf8')
    soup = BeautifulSoup(content, features="html.parser")
    paper_list = parser.parse(soup)
    return paper_list

def generate_web_page(cooked_paper_list, args):
    page = """
<!DOCTYPE html>
    <head>
        <title>%s</title>
    </head>
    <body>
    """ % args.conference

    template = """
        <div class="paper">
            <div class="title">%s</div>
            <div class="author">%s</div>
            <div class="link"><a href="%s">%s</a></div>
            <p>%s</p>
        </div>
        <hr />
    """
    for paper in cooked_paper_list:
        page += template % (paper[0], ', '.join(paper[3]), paper[2], paper[2], paper[1])
    return page + "</body></html>"

def generate_rss_page(cooked_paper_list, args):
    page = """<?xml version="1.0" encoding="utf8"?>
<rss version="2.0">
<channel>
    <title>nips2018</title>
    """

    template = """
    <item>
        <title>%s</title>
        <link>%s</link>
        <description>%s</description>
    </item>
    """
    for paper in cooked_paper_list:
        page += template % (paper[0], paper[2], paper[1])
    return page + "\n</channel>\n</rss>"



def main(args):
    try:
        parser = importlib.import_module("conference_template.%s" % args.conference).PaperListParser(args)
    except Exception as e:
        print(e)
        exit()

    paper_list = parse_paper_list(parser, args)
    parser.cook_paper(paper_list[0])
    cooked_paper_list = []
    for paper in tqdm.tqdm(paper_list):
        cooked_paper_list.append(parser.cook_paper(paper))
    
    web_page = generate_rss_page(cooked_paper_list, args)
    with open('rss_source/' + args.conference + '.xml', 'w', encoding='utf8') as f:
        f.write(web_page)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("RSS Helper")
    parser.add_argument("--conference", type=str)
    args = parser.parse_args()

    main(args)