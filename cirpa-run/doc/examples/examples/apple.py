from examples.fruits import StartFruits


class StartApple(StartFruits):

    fruit = "apple"

    def __init__(self):
        self.fruits += [self.fruit]
        self.add_argument("fruit", self.fruit)
