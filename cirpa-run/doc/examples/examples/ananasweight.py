from examples.fruits import StartFruits
from cirpa.hasharguments import Optional, RegExp


class StartAnanasWeight(StartFruits):

    fruit = "ananas"

    def __init__(self):
        self.fruits += [self.fruit]
        self.add_argument("fruit", self.fruit)
        self.add_argument("weight", RegExp("^[0-9]+( |)+[a-zA-Z]+"))
        self.add_argument("height", Optional(""))

    def execute(self, args):
        if "height" in args and args["height"]:
            print("hello world! We have a %s that weights %s and has the height of %s here!!" % (args["fruit"], args["weight"], args["height"]))
        else:
            print("hello world! We have a %s that weights %s here!!" % (args["fruit"], args["weight"]))

    def arguments(self, parser):
        StartFruits.arguments(self, parser)
        group = parser.add_argument_group('Ananas specific arguments')
        group.add_argument('--weight', dest="weight", type=RegExp)
        group.add_argument('--height', dest="height", required=False, type=Optional)
