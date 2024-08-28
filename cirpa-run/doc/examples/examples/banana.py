from examples.fruits import StartFruits


class StartBanana(StartFruits):

    fruit = "banana"

    def __init__(self):
        self.fruits += [self.fruit]
        self.add_argument("fruit", self.fruit)
