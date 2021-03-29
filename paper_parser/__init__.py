from .thecvf import CVFParser
from .mlr import MLRParser
from .ecva import ECVAParser
from .openreview import OpenreviewParser


def get_parser(args):
    if args.conference.lower() in ['cvpr', 'iccv']:
        assert (args.year % 2 == 1) and args.conference.lower() == 'iccv', \
            "ICCV only holds in odd years (Got: %d)" % args.year
        return CVFParser(args)
    elif args.conference.lower() == 'eccv':
        assert args.year % 2 == 0, "ECCV only holds in even years (Got: %d)" % args.year
        return CVFParser(args) if args.year < 2018 else ECVAParser(args)
    elif args.conference.lower() in ['nips', 'neurips']:
        return None
    elif args.conference.lower() in ['icml']:
        return MLRParser(args)
    elif args.conference.lower() == 'iclr':
        return OpenreviewParser(args)
    else:
        raise Exception('unknown conference: {}'.format(args.conference))
