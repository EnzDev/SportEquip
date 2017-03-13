from api.BaseApi import BaseApi
from dao import DAO
from json import *


class city(BaseApi):
    def __init__(self):
        super().__init__()
        self.supported = ["get"]

    def get(self, inp):
        city = ""
        try:
            city = inp["query"]["city"]
        except Exception:
            return (418, "Haaaaw (._.  )")
        r = DAO().guess_input_positions(city)
        return {
            "code": 200,
            "header": [],
            "content": "application/json",
            "res": str.encode(JSONEncoder().encode(r))
            }
