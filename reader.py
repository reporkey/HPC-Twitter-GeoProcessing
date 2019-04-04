import json
import numpy

class Reader:
    def __init__(self, args, n):
        self.gridFile = args.grid.name
        self.twittersFile = args.twitters.name
        self.grids = []  # A python list that contains all grids' boundaries
        self.num = {"A1": {"num": 0, "hashtags": {}}, "A2": {"num": 0, "hashtags": {}},
                    "A3": {"num": 0, "hashtags": {}}, "A4": {"num": 0, "hashtags": {}},
                    "B1": {"num": 0, "hashtags": {}}, "B2": {"num": 0, "hashtags": {}},
                    "B3": {"num": 0, "hashtags": {}}, "B4": {"num": 0, "hashtags": {}},
                    "C1": {"num": 0, "hashtags": {}}, "C2": {"num": 0, "hashtags": {}},
                    "C3": {"num": 0, "hashtags": {}}, "C4": {"num": 0, "hashtags": {}},
                    "C5": {"num": 0, "hashtags": {}}, "D3": {"num": 0, "hashtags": {}},
                    "D4": {"num": 0, "hashtags": {}}, "D5": {"num": 0, "hashtags": {}}}

    def grid_reader(self):
        with open(self.gridFile) as grid_json:
            # Filter raw geo info to only grids' boundaries
            data = json.load(grid_json)["features"]
            for grid in data:
                self.grids.append(grid["properties"])

    def search_line_index(self):
        with open(self.twittersFile, "r") as twitters_json:
            twitter_index = []
            while twitters_json.readline() != "":
                twitter_index.append(twitters_json.tell())
        return twitter_index

    def tweet_reader(self, chunks):
        with open(self.twittersFile, "r") as twitters_json:
            for each in chunks:
                twitters_json.seek(each)
                obj_str = twitters_json.readline()
                while len(obj_str) > 0 and obj_str[-1] != '}':
                    obj_str = obj_str[:-1]
                try:
                    obj = json.loads(obj_str)
                    self.count(obj)
                except:
                    continue

    def count(self, obj):
        loc = None
        loc = obj["doc"]["coordinates"]["coordinates"]
        if loc is None:
            loc = obj["doc"]["coordinates"]["coordinates"]
        if loc is None:
            loc = obj["value"]["geometry"]["coordinates"]
        if loc is None:
            loc = obj["doc"]["geo"]["coordinates"].reverse()
        if loc is None:
            return
        for grid in self.grids:
            if grid["xmin"] <= loc[0] <= grid["xmax"] and grid["ymin"] <= loc[1] <= grid["ymax"]:
                self.num[grid["id"]]["num"] += 1
                if obj["doc"]["retweeted"] != "false":  # ignore tag counting if its retweeted
                    text = obj["doc"]["text"]
                    hashtags = self.search_hashtag(text)
                    grid_hashtags = self.num[grid["id"]]["hashtags"]
                    for hashtag in hashtags:
                        grid_hashtags[hashtag] = grid_hashtags.get(hashtag, 0) + 1


    def search_hashtag(self, text):
        hashtags = []
        text = text.lower()
        for tag_from in range(2, len(text)):
            if text[tag_from-2:tag_from] == " #":
                for j in range(tag_from, len(text)):
                    if text[j] == " ":
                        if text[tag_from-1:j] not in hashtags:  # if unique
                            hashtags.append(text[tag_from-1:j])
                        break
        return hashtags

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