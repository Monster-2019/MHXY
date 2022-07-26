import numpy as np

def do_something_unreliable():
    a = np.array([[1,2,3], [1,2,3], [1,2,3], [1,2,3]])
    b = np.array([[1,2,4], [4,5,6], [4,5,6], [4,5,6]])
    return (a == b).sum()
    return (np.array(a) == np.array(b)).sum()
    

print(do_something_unreliable())