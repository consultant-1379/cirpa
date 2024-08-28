from cirpa.startbase import StartBase


class StartFruits(StartBase):

    goal = "fruits"
    fruits = []

    def execute(self, args):
        print("hello world! We have %s's here!!" % args["fruit"])

    def arguments(self, parser):
        parser.add_argument('--fruit', dest="fruit", choices=self.fruits)
