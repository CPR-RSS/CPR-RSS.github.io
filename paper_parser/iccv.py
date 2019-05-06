from paper_parser.cvpr import PaperListParser

class PaperListParser(PaperListParser):
    def __init__(self, args):
        super().__init__(args)
        self.base_url = "http://openaccess.thecvf.com/ICCV%s.py" % (args.year)
