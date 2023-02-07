# class Compute(object):

#     def __init__(self, number):
#         self.number = number

#     def add(self, x):
#         self.number += x

#     def reduce(self, x):
#         self.number -= x

#     def __call__(self, *argu, **kwargu):
#         # self.number += x * 2
#         self.add(*argu, **kwargu)

def test(a, b,**kwargu):
    print(a, b, kwargu)

test(1, b=3)