"""
    Define the base Api class useless alone, every api should extend it
"""


class BaseApi:
    """ The base Api class
        self.supported : List of supported methods. Any child must override the methods listed in self.supported
    """
    def __init__(self):
        self.supported = []  # By default no methods are supported, child will override this

    """ The four next methods will either :
            * return a dictionary as {
                "code":000,
                "header":[("headerName", "headerContent")],
                "content":"content/type",
                "res":str.encode("response")
                }
            * raise a tuple with (error, message, explanation)
    """
    def get(self, infile):
        pass

    def post(self, infile):
        pass

    def put(self, infile):
        pass

    def delete(self, infile):
        pass
