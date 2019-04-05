import json


class Reader:
    def __init__(self, args, n):
        self.gridFile = args.grid.name
        self.twittersFile = args.twitters.name
        self.grids = []  # A python list that contains grids' boundaries
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
            # abstract the grids' boundaries
            data = json.load(grid_json)["features"]
            for grid in data:
                self.grids.append(grid["properties"])

    def search_line_index(self):  # record line indexes in the whole file
        with open(self.twittersFile, "r") as twitters_json:
            twitter_index = []
            while twitters_json.readline() != "":
                twitter_index.append(twitters_json.tell())
        return twitter_index

    def tweet_reader(self, chunks):  # read and count tweet
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
        # check loc validity
        loc = []
        if "doc" in obj:
            if "coordinates" in obj["doc"]:
                if "coordinates" in obj["doc"]["coordinates"] and obj["doc"]["coordinates"]["type"] == "Point":
                    loc = obj["doc"]["coordinates"]["coordinates"]
            elif "geo" in obj["doc"]:
                if "coordinates" in obj["doc"]["geo"] and obj["doc"]["geo"]["type"] == "Point":
                    loc = obj["doc"]["geo"]["coordinates"].reverse()
        elif "value" in obj:
            if "geometry" in obj["value"]:
                if "coordinates" in obj["value"]["geometry"] and obj["value"]["geometry"]["type"] == "Point":
                    loc = obj["value"]["geometry"]["coordinates"]
        if loc is []:
            return
        for grid in self.grids:
            if grid["xmin"] <= loc[0] <= grid["xmax"] and grid["ymin"] <= loc[1] <= grid["ymax"]:
                self.num[grid["id"]]["num"] += 1
                if "text" in obj["doc"]:
                    text = obj["doc"]["text"]
                    hashtags = self.search_hashtag(text)
                    grid_hashtags = self.num[grid["id"]]["hashtags"]
                    for hashtag in hashtags:
                        grid_hashtags[hashtag] = grid_hashtags.get(hashtag, 0) + 1

    def search_hashtag(self, text):  # search and return hashtags from a string
        hashtags = []
        text = text.lower()
        tag_from = 0
        while tag_from < len(text):
            if text[tag_from-2:tag_from] == " #":
                for j in range(tag_from, len(text)):
                    if text[j] == " ":
                        if text[tag_from-1:j] not in hashtags:  # if unique
                            hashtags.append(text[tag_from-1:j])
                            tag_from = j
                        break
            tag_from += 1
        return hashtags
