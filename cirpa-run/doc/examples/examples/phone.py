from cirpa.startbase import StartBase
from cirpa.hasharguments import RegExp


class StartPhone(StartBase):

    phones = ["iPhone 6", "iPhone 7", "Nokia"]

    def __init__(self):
        self.add_argument("phone", RegExp("^[a-zA-Z]*"))

    def execute(self, args):
        print("hello world! We have %s phones here!!" % args["phone"])

    def arguments(self, parser):
        parser.add_argument('--phone', dest="phone", choices=self.phones, type=RegExp)
