from options import Options
from reader import Reader
from count import Count


def main(args):
    print("Grid file path: " + args.grid.name)
    print("Twitters file path: " + args.twitters.name)
    print("Parse Success")
    read = Reader(args)
    print("Read Success")
    count = Count(read)
    count.count_num()
    print(count.num)
    print("Num count Success")
    count.count_hashtags()
    print(count.hashtags)
    print("Hashtags count Success")
    print(count.hashtags[:5])


def run_parse():
    options = Options()
    args = options.parser.parse_args()
    main(args)


if __name__ == '__main__':
    run_parse()
