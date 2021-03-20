from .thecvf import TheCVFParser
from .mlr import  MlrParser


def get_parser(args):
    if args.conference.lowercase() in ['cvpr', 'iccv', 'eccv']:
        return TheCVFParser(args)
    elif args.conference.lowercase() in ['nips',]:
        return None
    elif args.conference.lowercase() in ['icml']:
        return MlrParser(args)
    else:
        raise Exception('unknown conference: %s'.format(args.conference))