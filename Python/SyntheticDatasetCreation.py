from skmine.datasets import make_transactions

# Generate your transactions
transactions = make_transactions(n_transactions=1000000, n_items=100, density=.80)

# Write to file
with open('A.dat', 'w') as f:
    for items in transactions:
        # Convert each item to a string and join them with ", "
        line = " ".join(map(str, items))
        f.write(line + '\n')