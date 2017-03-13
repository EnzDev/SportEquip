from api.BaseApi import BaseApi


class Login(BaseApi):
    def __init__(self):
        super().__init__()
        self.supported = []  # Do not add a method until it is fully implemented

    def post(self, infile):
        print(infile)

    def get(self, infile):
        print(infile)

