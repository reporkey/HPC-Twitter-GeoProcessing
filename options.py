import argparse
import os


class Options:

    def __init__(self):
        self.dirname = os.path.dirname(__file__)
        self._init_parser()

    def _init_parser(self):
        self.parser = argparse.ArgumentParser("Count the number of twitters from certain areas.")
        self.parser.add_argument('--grid',
                                 default=os.path.join(self.dirname, 'data\\melbGrid.json'), type=argparse.FileType('r'),
                                 help="Grid path.")
        self.parser.add_argument('--twitters',
                                 default=os.path.join(self.dirname, 'data\\new.json'), type=argparse.FileType('r'),
                                 help="Twitter path.")

