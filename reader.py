import json


class Reader:

    def __init__(self, args):
        self.gridFile = args.grid.name
        self.twittersFile = args.twitters.name
        self.grids = []  # A python list that contains all grids' boundaries
        self.twitters = []  # A python list that contains all twitters' objects
        with open(self.gridFile) as grid_json:
            # Filter raw geo info to only grids' boundaries
            data = json.load(grid_json)["features"]
            for grid in data:
                self.grids.append(grid["properties"])
        grid_json.close()
        with open(self.twittersFile) as twitters_json:
            data = json.load(twitters_json)["rows"]
            for tweet in data:
                self.twitters.append(tweet["doc"])
        twitters_json.close()

'''
zones structure: 
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
