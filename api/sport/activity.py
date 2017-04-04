from api.BaseApi import BaseApi
from dao import DAO
from JSONDecEncoder import JSONDecEncoder


class activity(BaseApi):
    def __init__(self):
        super().__init__()
        self.supported = ["get"]

    def get(self, inp):
        query = inp["query"]
        if("act" not in query):
            return 418, "Impossible de trouver l'activitée ou mauvais appel (._.  )"
        if("city" in query and "range" in query):
            r = DAO().guess_Activities_byGCity(query["city"], query["act"], int(query["range"]))
        else:
            if("city" in query):
                r = DAO().guess_Activities_byGCity(query["city"], query["act"])
            else:
                r = [act["ActLib"] for act in DAO().guess_input_activites(query["act"])]
        return {
            "code": 200,
            "header": [],
            "content": "application/json",
            "res": str.encode(JSONDecEncoder().encode(r))
            }
