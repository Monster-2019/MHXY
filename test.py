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

import json

with open("./data.json", 'r') as f:
    data = json.load(f)
    print(data)
    print(data == {})
    data['test'] = '123'

    with open('./data.json', 'w') as file:
        file.write(json.dumps(data, indent='\t'))