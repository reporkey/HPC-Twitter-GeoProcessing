class Count:

    def __init__(self, read):
        self.twitters = read.twitters
        self.grids = read.grids
        self.num = {"A1": {"num": 0, "hashtags": {}}, "A2": {"num": 0, "hashtags": {}},
                    "A3": {"num": 0, "hashtags": {}}, "A4": {"num": 0, "hashtags": {}},
                    "B1": {"num": 0, "hashtags": {}}, "B2": {"num": 0, "hashtags": {}},
                    "B3": {"num": 0, "hashtags": {}}, "B4": {"num": 0, "hashtags": {}},
                    "C1": {"num": 0, "hashtags": {}}, "C2": {"num": 0, "hashtags": {}},
                    "C3": {"num": 0, "hashtags": {}}, "C4": {"num": 0, "hashtags": {}},
                    "D3": {"num": 0, "hashtags": {}}, "D4": {"num": 0, "hashtags": {}}}

    def count(self):
        for tweet in self.twitters:
            loc = tweet["doc"]["coordinates"]["coordinates"]
            for grid in self.grids:
                if grid["xmin"] <= loc[0] <= grid["xmax"] and grid["ymin"] <= loc[1] <= grid["ymax"]:
                    self.num[grid["id"]]["num"] += 1
                    if tweet["doc"]["retweeted"] != "false":  # ignore tag counting if its retweeted
                        tweet_hashtags = tweet["doc"]["entities"]["hashtags"]
                        grid_hashtags = self.num[grid["id"]]["hashtags"]
                        for hashtag in tweet_hashtags:
                            grid_hashtags[hashtag["text"]] = grid_hashtags.get(hashtag["text"], 0) + 1
                    break

        # the type of hashtags are changed from dict to list of tuple, since dict doesn't have the order
        # for key in self.num:
        #     self.num[key]["hashtags"] = sorted(self.num[key]["hashtags"].items(), key= lambda a : a[1], reverse=True)
