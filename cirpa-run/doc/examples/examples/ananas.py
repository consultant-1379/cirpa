from examples.fruits import StartFruits


class StartAnanas(StartFruits):

    fruit = "ananas"

    def __init__(self):
        self.fruits += [self.fruit]
        self.add_argument("fruit", self.fruit)

    def execute(self, args):
        print("hello world! We have a %s here!!" % (args["fruit"]))

    def arguments(self, parser):
        StartFruits.arguments(self, parser)
