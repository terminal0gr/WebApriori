import os
import pandas as pd

# Convert list of lists to a DataFrame
data = [
    ["mineral water", "milk", "energy bar", "whole wheat rice", "green tea"],
    ["low fat yogurt"],
    ["whole wheat pasta", "french fries"],
    ["soup", "light cream", "shallot"],
    ["frozen vegetables", "spaghetti", "green tea"],
    ["french fries"],
    ["eggs", "pet food"],
    ["cookies"]
]

filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', 'sd.csv')
data = pd.read_csv(filepath, sep=',', header=None)

# Converting the list of lists into a DataFrame with transactions
df = pd.DataFrame(data)

# Display the DataFrame
print(df)