from paper_parser.cvpr import PaperListParser

class PaperListParser(PaperListParser):
    def __init__(self, args):
        super().__init__(args)
        assert args.year % 2 == 1, "ICCV only holds in the odd year"
        self.base_url = "http://openaccess.thecvf.com/ICCV%s.py" % (args.year)
