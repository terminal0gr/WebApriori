import skmine
from skmine.datasets import make_transactions

D = make_transactions(n_transactions=100,
                     n_items=10,
                     density=.2)

from skmine.datasets.utils import describe
print(describe(D))

print(type(D))
# print(D)