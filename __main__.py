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
    read.grid_reader()
    # if rank == 0:  # only the first process reading
    read.tweet_reader()

    # elif rank == 1:
    #     read.tweet_receiver(comm)

    count = Count(read)
    count.count()
    for area, value in count.num.items():
        print(area, ": ", value['num'], "; hashtags: ", value['hashtags'][:5])


def run_parse():
    options = Options()
    args = options.parser.parse_args()
    print("Grid file path: " + args.grid.name)
    print("Twitters file path: " + args.twitters.name)
    main(args)


if __name__ == '__main__':
    run_parse()
