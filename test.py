class Compute(object):

    def __init__(self, number):
        self.number = number

    def add(self, x):
        self.number += x

    def reduce(self, x):
        self.number -= x

    def __call__(self, *argu, **kwargu):
        # self.number += x * 2
        self.add(*argu, **kwargu)


compute = Compute(0)
compute(2)
compute.reduce(1)