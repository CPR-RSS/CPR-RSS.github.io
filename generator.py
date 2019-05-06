
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
