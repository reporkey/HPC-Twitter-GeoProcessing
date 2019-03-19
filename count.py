
class Count:

    def __init__(self, read):
        self.twitters = read.twitters
        self.grids = read.grids
        self.num = {"A1": 0, "A2": 0, "A3": 0, "A4": 0,
                    "B1": 0, "B2": 0, "B3": 0, "B4": 0,
                    "C1": 0, "C2": 0, "C3": 0, "C4": 0,
                    "D3": 0, "D4": 0}
        self.hashtags = {}

    def count_num(self):
        for tweet in self.twitters:
            loc = tweet["coordinates"]["coordinates"]
            for grid in self.grids:
                if grid["xmin"] <= loc[0] <= grid["xmax"] and grid["ymin"] <= loc[1] <= grid["ymax"]:
                    self.num[grid["id"]] += 1
                    break

    def count_hashtags(self):
        for tweet in self.twitters:
            if tweet["retweeted"] == "false":  # ignore if its retweeted
                continue
            hashtags = tweet["entities"]["hashtags"]
            for hashtag in hashtags:
                self.hashtags[hashtag["text"]] = self.hashtags.get(hashtag["text"], 0) + 1
        self.hashtags = sorted(self.hashtags.items(), key=lambda kv: kv[1],  reverse=True)

