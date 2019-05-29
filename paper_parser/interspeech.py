from __future__ import print_function
from urllib.request import urlopen
import re
import tqdm
from paper_parser import Paper

class PaperListParser(object):
	def __init__(self, args):
		self.base_url = "https://www.isca-speech.org/archive/Interspeech_%s/" % (args.year)

	def parse_paper_list(self, args):
		base_url = self.base_url
		content = urlopen(base_url).read().decode('utf8')
		papers = re.findall(r"<p><a class=\"w3-text\"[^\n]+<br>", content)

		overall = 0
		failed = 0
		paper_list = []
		for paper in tqdm.tqdm(papers):
			try:
				title = re.search(r'\">([^\n]+)</a', paper).group(1)
				idx = re.search(r'href=\"abstracts/(\d+)\.html\"', paper).group(1)
				paper_list.append((title, idx))
				overall += 1
			except:
				failed += 1
		print("Parse %s; Overall: %d, faild: %d " % (self.base_url, overall, failed))
		return paper_list

	def cook_paper(self, paper_info):
		try:
			title = paper_info[0]
			idx = paper_info[1]
			abstract_url = self.base_url + "abstracts/" + str(idx) + ".html"
			abstract_page = urlopen(abstract_url).read().decode('utf8')
			abstract = re.search(r"<p>([^<]+)</p>", abstract_page).group(1)
			abstract = self.text_process(abstract)

			pdf_url = self.base_url + "pdfs/" + str(idx) + ".pdf"

			author_list = re.search(r"<h4 class=\"w3-center\">([^\n]+)</h4>", abstract_page).group(1)
			author_list = author_list.split(',')
			author_list = [self.text_process(x) for x in author_list]
			return Paper(self.text_process(title), abstract, pdf_url, author_list)
		except Exception as e:
			print(e)
			return (paper_info[0], e, self.base_url, [])

	@staticmethod
	def text_process(text):
		text = text.replace('&', "&amp;")
		text = text.replace("<", "&lt;")
		text = text.replace('>', "&gt;")
		text = text.replace("'", "&apos;")
		text = text.replace('"', "&quot;")
		return text
