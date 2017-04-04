from api.BaseApi import BaseApi
from dao import DAO
from JSONDecEncoder import JSONDecEncoder


class city(BaseApi):
    def __init__(self):
        super().__init__()
        self.supported = ["get","post"]

    def get(self, inp):
        query = inp["query"]
        if("city" not in query):
            return 418, "Impossible de trouver la ville ou mauvais appel (._.  )"
        if("act" in query):
            r = DAO().guess_City_byGActivity(query["city"], query["act"])
        else:
            r = DAO().guess_input_positions(query["city"])
        return {
            "code": 200,
            "header": [],
            "content": "application/json",
            "res": str.encode(JSONDecEncoder().encode(r))
            }
    def post(self, inp):
        if("city" in inp["data"].keys()):
            return {
                "code": 200,
                "header": [],
                "content": "application/json",
                "res": str.encode(JSONDecEncoder().encode(DAO().get_City_Pos(inp["data"].getvalue("city"))))
            }
        return 418, "wait !!"