import argparse


class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        self.parser = argparse.ArgumentParser("Count the number of twitters from certain areas.")
        self.parser.add_argument('--grid',
                                 default='./data/melbGrid.json',
                                 type=argparse.FileType('r'),
                                 help="Grid path.")
        self.parser.add_argument('--twitters',
                                 default='./data/tinyTwitter.json',
                                 type=argparse.FileType('r'),
                                 help="Twitter path.")
