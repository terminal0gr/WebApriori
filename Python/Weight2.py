# Initialize the list and dictionary
keys_list = ["customer_id", "invoice_no", "inv", "age", "category", "quantity", "invoice_date", "item_id", "shopping_mall"]
value_dict = {
    "invoice": 10, 
    "inv": 10, 
    "no": 5,
    "item": 7,
    "id": 3
}

# Function to check if any dictionary key is a substring of the given string
def get_value_from_substrings(s, value_dict):
    total_value = 0
    for key, value in value_dict.items():
        if key.lower() in s:
            total_value += value
    return total_value

# Create the resulting dictionary
result_dict = {}
for key in keys_list:
    value = get_value_from_substrings(key, value_dict)
    if value > 0:  # Only add entries that have non-zero values
        result_dict[key] = value

if 
# Sort the dictionary
# First by value in descending order, then by position in the original list in ascending order
sorted_result = dict(sorted(result_dict.items(), key=lambda x: (-x[1], keys_list.index(x[0]))))

# Print the sorted dictionary
print(sorted_result)