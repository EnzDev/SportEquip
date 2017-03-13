from api.BaseApi import BaseApi
from json import *


class Example(BaseApi):
    def __init__(self):
        super().__init__()
        self.supported = ["post", "get", "delete", "get"]
        self.encoder = JSONEncoder()
        self.decoder = JSONDecoder()

    def post(self, infile):
        return {
                "code": 200,
                "header": [],
                "content": "application/json",
                "res": str.encode(self.encoder.encode(infile["query"]))
                }

    def put(self, infile):
        super().put(infile)

    def delete(self, infile):
        super().delete(infile)

    def get(self, infile):
        return {
            "code": 200,
            "header": [],
            "content": "application/json",
            "res": str.encode(self.encoder.encode({"ip": infile["client"][0]}))
        }
