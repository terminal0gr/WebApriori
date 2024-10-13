import skmine
from skmine.datasets import make_transactions

# synthetic data creation
def syntheticDataCreation():

    # With a binary matrix representation of the resulting dataset, we have the following equality
    #     .. math:: density = { Number\ of\ ones \over Number\ of\ cells }
    # This is equivalent to
    #     .. math:: density = { Average\ transaction\ size \over number\ of\ items

    D = make_transactions(n_transactions=10,
                        n_items=20,
                        density=.2)

    from skmine.datasets.utils import describe
    print(describe(D))

    print(type(D))
    print(D)
    return D

syntheticDataCreation()



