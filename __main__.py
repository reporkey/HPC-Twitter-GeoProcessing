from mpi4py import MPI
import math
import numpy

from options import Options
from reader import Reader


def add_result(obj1, obj2, datatype):
    # reduce num
    for area_id in obj2:
        if area_id in obj1:
            obj1[area_id]["num"] += obj2[area_id]["num"]
        else:
            obj1[area_id] = obj2[area_id]
    # reduce hashtag
    for area_id in obj2:
        if area_id in obj1:  # matching area
            for tag in obj2[area_id]["hashtags"]:
                if tag in obj1[area_id]["hashtags"]:  # matching hashtags
                    obj1[area_id]["hashtags"][tag] += obj2[area_id]["hashtags"][tag]
                else:
                    obj1[area_id]["hashtags"][tag] = obj2[area_id]["hashtags"][tag]
    return obj1


def divide_index(lists, n):
    chunks = []
    size = math.ceil(len(lists) / n)
    for i in range(0, n):
        chunks.append(lists[i*size: (i+1)*size])
    return chunks


def main(args):
    # init MPI
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    read = Reader(args, size)
    read.grid_reader()

    # divide index lists into n chunks evenly
    chunks = []
    if rank == 0:
        twitter_index = read.search_line_index()
        chunks = divide_index(twitter_index, size)
    # scatter indexes to each processor, assigning jobs to them
    chunks = comm.scatter(chunks)
    read.tweet_reader(chunks)
    comm.barrier()

    # gather count result to master
    sum_op = MPI.Op.Create(add_result, commute=True)
    read.num = comm.reduce(read.num, op=sum_op)

    # sort and print on master
    if rank == 0:
        # sort hashtags
        for area_id, value in read.num.items():
            value["hashtags"] = sorted(value["hashtags"].items(), key=lambda a: a[1], reverse=True)
        # sort number
        read.num = sorted(read.num.items(), key=lambda a: a[1]["num"], reverse=True)
        # print number
        print("The total number of Twitter in each area.")
        for i in range(0, len(read.num)):
            if i != len(read.num) - 1:
                print(read.num[i][0] + ": " + str(read.num[i][1]["num"]) + " posts, ")
            else:
                print(read.num[i][0] + ": " + str(read.num[i][1]["num"]) + " posts")
        # print hashtags
        print("\nTop 5 hashtags in each area.")
        for area in read.num:
            fifth = 4
            unique = []
            len(unique)
            while len(unique) < 5 and fifth < len(area[1]["hashtags"]):
                fifth += 1
                unique = []
                for each in area[1]["hashtags"][: fifth]:
                    unique.append(each[1])
                unique = numpy.unique(unique)
            print(area[0]+": "+str(tuple((area[1]["hashtags"])[:fifth]))
                  .replace("', ", ",").replace("('#", "(#").replace(" ", ""))


def run_parse():
    # parse optional arguments in commend line (e.g. path of file)
    options = Options()
    args = options.parser.parse_args()
    main(args)


if __name__ == '__main__':
    run_parse()
