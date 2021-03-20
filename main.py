import importlib

import tqdm

import generator


def main(args):
    # first, we construct a paper parser
    try:
        _parser = importlib.import_module("paper_parser.%s" % args.conference).PaperListParser(args)
    except Exception as e:
        print(e), exit()
    # second, we parse and generate a paper list containing paper information
    paper_list = _parser.parse_paper_list(args)

    # Third, parse detail paper information one by one
    cooked_paper_list = []
    for paper in tqdm.tqdm(paper_list):
        cooked_paper_list.append(_parser.cook_paper(paper))
    # cooked_paper_list.append(_parser.cook_paper(paper_list[0]))

    # Finally, generate output to a file
    _generator = getattr(generator, 'generate_%s_page' % (args.outputformat))
    content_page = _generator(cooked_paper_list, args)
    with open('%s_source/' % (args.outputformat) + args.conference + str(args.year) + '.xml',
              'w', encoding='utf8') as f:
        f.write(content_page)


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser("RSS Helper")
    parser.add_argument("--conference", '-c', help='Conference name(NIPS for NeurIPS)', type=str)
    parser.add_argument('--year', '-y', help='Specific year', type=int)
    parser.add_argument('--outputformat', '-o', help='Output format', type=str, default='rss')
    parser.add_argument('--multiprocessing', '-m', help='Number of Workers', type=int, default=0)
    args = parser.parse_args()

    main(args)
