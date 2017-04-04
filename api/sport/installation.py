from api.BaseApi import BaseApi
from dao import DAO
from JSONDecEncoder import JSONDecEncoder


class installation(BaseApi):
    def __init__(self):
        super().__init__()
        self.supported = ["get"]

    def get(self, inp):
        query = inp["query"]
        if ("city" not in query):
            return 418, "Impossible de trouver les installations sans ville ou mauvais appel (._.  )"
        if ("city" in query and "range" in query and "act" in query):
            r = DAO().get_installation(query["city"], query["act"], int(query["range"]))
        else:
            if ("city" in query and "range" in query and "act" not in query):
                r = DAO().get_installation(query["city"], "", int(query["range"]))
            else:
                if ("city" in query and "range" not in query and "act" in query):
                    r = DAO().get_installation(query["city"], query["act"])
                else:  # "city" in query and "range" not in query and "act" not in query
                    r = DAO().get_installation(query["city"], "")
        return {
            "code": 200,
            "header": [],
            "content": "application/json",
            "res": str.encode(JSONDecEncoder().encode(r))
        }
