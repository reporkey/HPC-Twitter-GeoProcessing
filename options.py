import argparse
import os


class Options:

    def __init__(self):
        self.dirname = os.path.dirname(__file__)
        self._init_parser()

    def _init_parser(self):
        self.parser = argparse.ArgumentParser("Count the number of twitters from certain areas.")
        self.parser.add_argument('--grid',
                                 default=os.path.join(self.dirname, 'data\\melbGrid.json'),
                                 type=argparse.FileType('r'),
                                 help="Grid path." + os.path.join(self.dirname, 'data\\melbGrid.json'))
        self.parser.add_argument('--twitters',
                                 default=os.path.join(self.dirname, 'data\\tinyTwitter.json'),
                                 type=argparse.FileType('r'),
                                 help="Twitter path.Default=" + os.path.join(self.dirname, 'data\\tinyTwitter.json'))
        self.parser.add_argument('--chunks',
                                 default=32,
                                 type=int,
                                 help="Number of tweet entities in the each chunck. Default=100000")
