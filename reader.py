import json
import ijson
from ijson.common import ObjectBuilder
import os
import math

class Reader:

    def __init__(self, args):
        self.gridFile = args.grid.name
        self.twittersFile = args.twitters.name
        self.twitter_index = []
        # Since it's hard to measure the density of tweet entities in big file. So we assume that it has the same
        # density as small file.  density = num of tweets per file byte
        density = 7000 / 24952156
        file_size = os.stat(self.twittersFile).st_size
        self.entities = math.floor(file_size * density / args.chunks)  # num of entities in each chunk
        self.grids = []  # A python list that contains all grids' boundaries
        self.twitters = []  # A python list that contains all twitters' objects

    def grid_reader(self):
        with open(self.gridFile) as grid_json:
            # Filter raw geo info to only grids' boundaries
            data = json.load(grid_json)["features"]
            for grid in data:
                self.grids.append(grid["properties"])

    # def tweet_receiver(self, comm):
    #     data = comm.recv(source=0)
    #     print('On', comm.Get_rank(), ', data is ', data)

    def search_line_index(self):
        with open(self.twittersFile, "r") as twitters_json:
            while twitters_json.readline() != "":
                self.twitter_index.append(twitters_json.tell())


    def tweet_reader(self, indexes):
        with open(self.twittersFile, "r") as twitters_json:
            for each in indexes:
                twitters_json.seek(each)
                obj_str = twitters_json.readline()
                while len(obj_str) > 0 and obj_str[-1] != '}':
                    obj_str = obj_str[:-1]
                try:
                    obj = json.loads(obj_str)
                    self.twitters.append(obj)
                except:
                    continue





'''
Method 0: Using json.load to read whole json file. It's the easiest and fastest(not 
tested), but out of memory might be happened.
'''
            # self.twitters = json.load(twitters_json)["rows"]

'''
Method 1: Using ijson.items extracts all 'doc' objects. It does not allow extracts some
part of 'doc'. It can reduce some size, but depending on the structure, the 'doc' 
still can be quite large.
'''
            # self.twitters = ijson.items(twitters_json, 'rows.item.doc')

'''
Method 2: Using ijson.parse to read and filter out 'doc' object only, stored in a list. 
The benefit is that it allows us to read 'doc' separately, which gives more options on
memory management. But in the meanwhile, ijson.parse largely increases the runtime. 
There are lots of comparisons.
'''
            # parser = ijson.parse(twitters_json)
            # for prefix, event, value in parser:
            #     if (prefix, event, value) == ('rows.item', 'map_key', 'doc'):
            #         doc = ObjectBuilder()
            #     elif prefix.startswith('rows.item.doc'):
            #         doc.event(event, value)
            #     elif (prefix, event) == ('rows.item', 'end_map'):
            #         self.twitters.append(doc.value)

'''
Method 3: Using ijson.parse to read and filter out 'coordinates', 'hashtags' and 
'retweeted' objects. Comparing with Method 2, this hugely save the space. The data is 
unlikely be oversized in this scope of project. However, it also takes long time. Not 
sure about the efficiency between Method 2 and Method 3.
'''
            # parser = ijson.parse(twitters_json)
            # for prefix, event, value in parser:
            #     # in 'doc.coordinates' object
            #     if (prefix, event, value) == ('rows.item.doc', 'map_key', 'coordinates'):
            #         coordinate = ObjectBuilder()
            #     elif prefix.startswith('rows.item.doc.coordinates'):
            #         coordinate.event(event, value)
            #     # in 'doc.retweeted' object
            #     elif (prefix, event, value) == ('rows.item.doc', 'map_key', 'retweeted'):
            #         retweeted = ObjectBuilder()
            #     elif prefix.startswith('rows.item.doc.retweeted'):
            #         retweeted.event(event, value)
            #     # in 'doc.entities.hashtags' object
            #     elif (prefix, event, value) == ('rows.item.doc.entities', 'map_key', 'hashtags'):
            #         hashtag = ObjectBuilder()
            #     elif prefix.startswith('rows.item.doc.entities.hashtags'):
            #         hashtag.event(event, value)
            #     # at the end of this tweet, record (cood, hashtag, retweeted) into twitters
            #     elif (prefix, event) == ('rows.item.doc', 'end_map'):
            #         self.twitters.append({'coordinate': coordinate.value,
            #                          'hashtag': hashtag.value,
            #                          'retweeted': retweeted.value})

'''
grids structure: 
[
    { 
        "type": "Feature", 
        "properties": { 
            "id": "A1", 
            "xmin": 144.700000, 
            "xmax": 144.850000, 
            "ymin": -37.650000, 
            "ymax": -37.500000 
        }, 
        "geometry": { 
            "type": "Polygon", 
            "coordinates": [ 
                [ 
                    [ 144.7, -37.5 ], 
                    [ 144.85, -37.5 ], 
                    [ 144.85, -37.65 ], 
                    [ 144.7, -37.65 ], 
                    [ 144.7, -37.5 ] 
                ] 
            ] 
        } 
    },
    ...
]

Twitters structure:
{ 
    ...
    "row": {
        [
            "doc" : {
                "_id" : "570379215192727552",
                "value" : {
                    "type":"Feature",
                    "geometry":{
                        "type":"Point",
                        "coordinates":[144.92340088,-37.95935781]
                    }, 
                "entities" : {
                    "hashtags" : [
                        {"indices":[95,105],"text":"melbourne"}
                    ]
                }
            }
        ]
        ...
    }
}
'''

'''
size of tinyTwitter.json file: 3580480
entities in tinyTwitter.json file: 1000

size of smallTwitter.json file: 24952156
entities in smallTwitter.json file: 7000

size of bigTwitter.json file: 10948035094
estimated entities in bigTwitter.json file: 3071327

'''