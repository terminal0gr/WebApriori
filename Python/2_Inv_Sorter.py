class Inv_2_Sorter:
    def __init__(self, keys_list, value_dict):
        self.keys_list = keys_list
        self.value_dict = value_dict
    
    def get_value_from_substrings(self, s):
        """
        Sum the values from the dictionary if any part of the dictionary's keys
        is a substring of the given string.
        """
        total_value = 0
        for key, value in self.value_dict.items():
            if key in s:
                total_value += value
        return total_value

    def generate_sorted_dict(self):
        """
        Generate a dictionary with keys from the keys_list and values from the value_dict,
        sorted by value in descending order and by original list position in ascending order.
        """
        # Create the resulting dictionary
        result_dict = {}
        for key in self.keys_list:
            value = self.get_value_from_substrings(key)
            if value > 0:  # Only add entries that have non-zero values
                result_dict[key] = value
        
        # Sort the dictionary
        # First by value in descending order, then by position in the original list in ascending order
        sorted_result = dict(sorted(result_dict.items(), key=lambda x: (-x[1], self.keys_list.index(x[0]))))
        
        return sorted_result

# Example usage
keys_list = ["customer_id", "invoice_no", "inv", "age", "category", "quantity", "invoice_date", "item_id", "shopping_mall"]
value_dict = {
    "invoice": 10, 
    "inv": 10, 
    "no": 5,
    "item": 7,
    "id": 3
}

# Create an instance of DictionarySorter
sorter = Inv_2_Sorter(keys_list, value_dict)

# Get the sorted dictionary
sorted_dict = sorter.generate_sorted_dict()

# Print the result
print(sorted_dict)