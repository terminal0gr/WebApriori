import skmine
from skmine.datasets import make_transactions
from skmine.datasets.utils import describe
import pandas as pd
import csv

# synthetic data creation
def syntheticDataCreation(n_transactions,n_items,density,filepath=None):

    # With a binary matrix representation of the resulting dataset, we have the following equality
    #     .. math:: density = { Number\ of\ ones \over Number\ of\ cells }
    # This is equivalent to
    #     .. math:: density = { Average\ transaction\ size \over number\ of\ items

    D = make_transactions(n_transactions,n_items,density)

    # df = pd.Series.to_frame(D)

    # Write to file with ';' delimiter and UTF-8 encoding
    if filepath is not None:
        # Convert lists to semicolon-separated strings
        series_str = D.apply(lambda x: ';'.join(map(str, x)))
        if str(filepath).upper()=="DEFAULT":
            filepath="T" + str(int(n_items*density)) + "IT" + str(n_items) + "D" + str(n_transactions) + ".csv"
        # Manually write the Series to a CSV file
        with open(filepath, 'w', encoding='utf-8') as f:
            for row in series_str:
                f.write(f"{row}\n")
    else:
        print(describe(D))
        print(type(D))
        print(D)
        return D

syntheticDataCreation(n_transactions=200000,n_items=2000,density=0.2,filepath="default")



