from collections import defaultdict, namedtuple

class FPTree:
    Route = namedtuple('Route', ['head', 'tail'])

    def __init__(self):
        self.root = FPNode(None, None)
        self.routes = {}

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
        """Updates the route of an item in the FP-Tree."""
        if node.item in self.routes:
            route = self.routes[node.item]
            route.tail.neighbor = node
            self.routes[node.item] = self.Route(route.head, node)
        else:
            self.routes[node.item] = self.Route(node, node)

    def find_prefix_paths(self, item):
        """Finds all prefix paths for a given item."""
        paths = []
        node = self.routes[item].head
        while node:
            path = []
            current_node = node
            while current_node.parent and current_node.parent.item is not None:
                path.append(current_node.parent.item)
                current_node = current_node.parent
            if path:
                paths.append((list(reversed(path)), node.count))
            node = node.neighbor
        return paths

    def mine_patterns(self, minimum_support):
        """Mines the frequent patterns from the FP-Tree."""
        patterns = {}
        for item, route in sorted(self.routes.items(), reverse=True, key=lambda x: x[0]):
            # Get total support for this item
            support = sum(node.count for node in self.get_nodes(item))
            if support >= minimum_support:
                patterns[frozenset([item])] = support

            conditional_patterns = self.find_prefix_paths(item)
            conditional_tree = self.build_conditional_tree(conditional_patterns)

            sub_patterns = conditional_tree.mine_patterns(minimum_support)
            for pattern, count in sub_patterns.items():
                pattern = frozenset([item]).union(pattern)
                patterns[pattern] = count

        return patterns

    def get_nodes(self, item):
        """Yields all nodes in the FP-Tree for the given item."""
        node = self.routes[item].head
        while node:
            yield node
            node = node.neighbor

    def build_conditional_tree(self, conditional_patterns):
        """Builds a conditional FP-Tree from prefix paths."""
        tree = FPTree()
        for path, count in conditional_patterns:
            tree.add_transaction(path, count)
        return tree


class FPNode:
    """Represents a node in the FP-Tree."""
    def __init__(self, item, parent, count=1):
        self.item = item
        self.count = count
        self.parent = parent
        self.neighbor = None
        self.children = {}

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
    tree = FPTree()
    item_support = defaultdict(int)

    # First pass: count item frequencies across all transactions
    for transaction in transactions:
        for item in transaction:
            item_support[item] += 1

    # Filter out items below the minimum support threshold
    frequent_items = {item for item, count in item_support.items() if count >= minimum_support}

    # Second pass: sort transactions by item frequency and build the FP-Tree
    for transaction in transactions:
        sorted_transaction = [item for item in transaction if item in frequent_items]
        sorted_transaction.sort(key=lambda item: item_support[item], reverse=True)
        tree.add_transaction(sorted_transaction)

    # Mine frequent patterns from the FP-Tree
    patterns = tree.mine_patterns(minimum_support)
    return patterns


# Example usage
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
    
    # Sort the patterns by support, then by the itemset
    sorted_patterns = sorted(patterns.items(), key=lambda x: (-x[1], sorted(x[0])))

    idx=0
    for pattern, support in sorted_patterns:
        print(idx, support, pattern)
        idx+=1

