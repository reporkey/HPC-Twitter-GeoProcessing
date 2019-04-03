from mpi4py import MPI
import math

from options import Options
from reader import Reader
from count import Count


def add_counter(counter1, counter2, datatype):
    for item in counter2:
        if item in counter1:
            counter1[item] += counter2[item]
        else:
            counter1[item] = counter2[item]
    return counter1


def chunk_list(lists, n):
    chunks = []
    size = math.ceil(len(lists) / n)
    for i in range(0, n):
        down = i*size
        if (i+1)*size < len(lists):
            up = (i + 1) * size
        else:
            up = len(lists) - 1
        chunks.append(lists[i*size:(i+1)*size])
    return chunks


def main(args):
    # init MPI
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    read = Reader(args)
    read.grid_reader()

    # split lists into n chunks evenly
    chunks = []
    if rank == 0:
        read.search_line_index()
        chunks = chunk_list(read.twitter_index, size)
    # scatter indexes to each processor, assigning jobs to them
    chunks = comm.scatter(chunks)
    read.tweet_reader(chunks)

    count = Count(read)
    count.count()
    # gather number count result to master
    counter_sum_op = MPI.Op.Create(add_counter, commute=True)
    for area, value in count.num.items():
        value["num"] = comm.reduce(value["num"], op=MPI.SUM)
        value["hashtags"] = comm.allreduce(value["hashtags"], op=counter_sum_op)

    if rank == 0:
        # sort hashtags by key after all count
        for key in count.num:
            count.num[key]["hashtags"] = sorted(count.num[key]["hashtags"].items(), key= lambda a : a[1], reverse=True)
        for area, value in count.num.items():
            print(area, ": ", value['num'], "; hashtags: ", value['hashtags'][:5])

def run_parse():
    options = Options()
    args = options.parser.parse_args()
    main(args)


if __name__ == '__main__':
    run_parse()
