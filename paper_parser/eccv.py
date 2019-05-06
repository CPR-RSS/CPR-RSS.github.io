from paper_parser.cvpr import PaperListParser

class PaperListParser(PaperListParser):
    def __init__(self, args):
        super().__init__(args)
        assert args.year % 2 == 0, "ECCV only holds in the even year"
        self.base_url = "http://openaccess.thecvf.com/ECCV%s.py" % (args.year)
