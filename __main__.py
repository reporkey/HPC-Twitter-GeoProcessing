from mpi4py import MPI
import numpy

from options import Options
from reader import Reader
from count import Count


def main(args):

    # init MPI
    # comm = MPI.COMM_WORLD
    # size = comm.Get_size()
    # rank = comm.Get_rank()

    read = Reader(args)
    print(read.entities)
    # read.grid_reader()
    # if rank == 0:  # only the first process reading
    # read.tweet_reader()

    # print(len(read.twitters))
    # elif rank == 1:
    #     read.tweet_receiver(comm)



    # print("Read Success")
    # count = Count(read)
    # count.count()
    # print(count.num)
    # print("Num count Success")
    # count.count_hashtags()
    # print(count.hashtags)
    # print("Hashtags count Success")
    # print(count.hashtags[:5])


def run_parse():
    options = Options()
    args = options.parser.parse_args()
    print("Grid file path: " + args.grid.name)
    print("Twitters file path: " + args.twitters.name)
    print("Parse Success")
    main(args)


if __name__ == '__main__':
    run_parse()
