import sys
import os
import json

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
            s=s.lower()
            if key.lower() in s:
                total_value += value
        return total_value

    def generate_best_item(self):
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
        
        if sorted_result:
            return next(iter(sorted_result))
        else:
            return '?'

# Example usage
# keys_list = ["customer_id", "invoice_no", "inv", "age", "category", "quantity", "invoice_date", "item_id", "shopping_mall"]
# value_dict = {
#     "invoice": 10, 
#     "inv": 10, 
#     "no": 5,
#     "item": 7,
#     "id": 3
# }

# filepath=os.path.join('datasets')	
        
# #Firstly I check if the folder exists. If not, then create it and auto detect dataset attributes.
# if not os.path.exists(filepath):
#     print(f"Failed to detect datasets folder!!!")     
#     sys.exit    

# filepath=os.path.join('datasets', 'Inc_2_Group_Words.json')	
# #Secondly I check if the the lexicon file exists. If not
# if not os.path.exists(filepath): 
#     print(None)
# else:

#     value_dict=None

#     # Open the JSON file in read mode
#     with open(filepath, encoding='utf-8-sig') as file:
#         # Load the JSON data from the file
#         value_dict = json.load(file)

#     if value_dict is None:
#         print(None)
#         sys.exit()

#     # Create an instance of DictionarySorter
#     sorter = Inv_2_Sorter(keys_list, value_dict)

#     # Print the result
#     print(sorter.generate_best_item())