from collections import defaultdict, namedtuple
import pandas as pd
import sys
sys.setrecursionlimit(200000)  # Adjust the value as needed

class FPTree:
    Route = namedtuple('Route', ['head', 'tail'])

    def __init__(self):
        self.root = FPNode(None, None)  # Root of the FP-Tree
        self.routes = {}  # A dictionary to track nodes of each item

    def add_transaction(self, transaction, count=1):
        """Adds a transaction to the FP-Tree."""
        current_node = self.root
        for item in transaction:
            next_node = current_node.search(item)
            if next_node:
                next_node.increment(count)
            else:
                next_node = FPNode(item, current_node, count)
                current_node.add(next_node)
                self.update_route(next_node)
            current_node = next_node

    def update_route(self, node):
        """Updates the route of an item in the FP-Tree without recursion."""
        if node.item in self.routes:
            # Append the node to the existing route
            route = self.routes[node.item]
            route.tail.neighbor = node  # Link the new node as the neighbor of the last one
            self.routes[node.item] = self.Route(route.head, node)  # Update the tail of the route
        else:
            # Create a new route if this is the first occurrence of the item
            self.routes[node.item] = self.Route(node, node)

    def find_prefix_paths(self, item):
        """Finds all prefix paths for a given item."""
        if item not in self.routes:
            return []

        paths = []
        node = self.routes[item].head
        while node:
            path = []
            current_node = node
            while not current_node.is_root():
                path.append(current_node.item)
                current_node = current_node.parent
            path.reverse()  # Reverse the path to have it in the correct order
            if path:
                paths.append((path[:-1], node.count))  # Exclude the item itself in the path
            node = node.neighbor
        return paths

    def mine_patterns(self, minimum_support):
        """Mines the frequent patterns from the FP-Tree."""
        patterns = {}
        for item in self.routes.keys():
            # Sum up the total support for the item
            support = sum(node.count for node in self.get_nodes(item))
            if support >= minimum_support:
                patterns[(item,)] = support
                conditional_patterns = self.find_prefix_paths(item)
                conditional_tree = self.build_conditional_tree(conditional_patterns)
                sub_patterns = conditional_tree.mine_patterns(minimum_support)
                for pattern, count in sub_patterns.items():
                    patterns[(item,) + pattern] = count
        return patterns

    def get_nodes(self, item):
        """Yields all nodes in the FP-Tree for the given item."""
        node = self.routes[item].head
        while node:
            yield node
            node = node.neighbor

    def build_conditional_tree(self, conditional_patterns):
        """Builds a conditional FP-Tree."""
        tree = FPTree()
        for path, count in conditional_patterns:
            tree.add_transaction(path, count)
        return tree


class FPNode:
    """Represents a node in the FP-Tree."""
    def __init__(self, item, parent, count=1):
        self.item = item  # The item stored in the node
        self.count = count  # Count of transactions sharing this node
        self.parent = parent  # Parent node in the FP-Tree
        self.neighbor = None  # Link to the next node with the same item
        self.children = {}  # Dictionary of children nodes

    def is_root(self):
        """Returns True if the node is the root of the tree."""
        return self.item is None

    def search(self, item):
        """Searches for a child node with the given item."""
        return self.children.get(item)

    def add(self, child_node):
        """Adds a child node to this node."""
        self.children[child_node.item] = child_node

    def increment(self, count):
        """Increments the count of the node."""
        self.count += count


def find_frequent_itemsets(transactions, minimum_support):
    """Finds frequent itemsets in the transaction database."""
    # Build the initial FP-Tree
    tree = FPTree()
    item_support = defaultdict(int)

    # Count item frequencies across all transactions
    for transaction in transactions:
        for item in transaction:
            item_support[item] += 1

    # Keep only items that meet the minimum support threshold
    frequent_items = {item for item, count in item_support.items() if count >= minimum_support}

    # Sort transactions by item frequency in descending order and add to the tree
    for transaction in transactions:
        sorted_transaction = [item for item in transaction if item in frequent_items]
        sorted_transaction.sort(key=lambda item: item_support[item], reverse=True)
        tree.add_transaction(sorted_transaction)

    # Mine frequent patterns from the tree
    return tree.mine_patterns(minimum_support)


# Example usage:
if __name__ == "__main__":
    transactions = [
        ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
        ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
        ['b', 'f', 'h', 'j', 'o', 'p'],
        ['b', 'c', 'k', 's', 'p'],
        ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
    ]
    minimum_support = 3
    patterns = find_frequent_itemsets(transactions, minimum_support)
    # print(patterns)

    for index, (key, value) in enumerate(patterns.items()):
        # Join the tuple key into a string
        key_string = ','.join(key)
        # Print the formatted output
        print(f"{index}\t{key_string}\t{value}")
    