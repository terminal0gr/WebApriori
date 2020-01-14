# Main Apriori engine.
def webApriori(itemsets, **kwargs):
    """
    Executes Apriori algorithm and returns an association rules generator.

    Arguments:
        itemsets -- A itemset iterable object (example [['A', 'B'], ['B', 'C']]).

    Keyword arguments:
        min_support -- The minimum support of association_rules (float).
        min_confidence -- The minimum confidence of association_rules (float).
        min_lift -- The minimum lift of association_rules (float).
        max_length -- The maximum length of the association_rule (integer).
    """
    # Parse the arguments.
    min_support = kwargs.get('min_support', 0.1)
    min_confidence = kwargs.get('min_confidence', 0.2)
    min_lift = kwargs.get('min_lift', 1.5)
    max_length = kwargs.get('max_length', 4)
    
    rules_counter=0
    global max_rules

    # Check arguments.
    if min_support <= 0:
        raise ValueError('minimum support can''t be negative number!!!')
    if min_confidence <= 0:
        raise ValueError('minimum confidence can''t be negative number!!!')    
    if min_lift <= 0:
        raise ValueError('minimum lift can''t be negative number!!!') 
    if max_length < 2:
        raise ValueError('Rules max length can''t be negative number!!!') 

    # Calculate supports.
    itemset_manager = itemsetManager.create(itemsets)
    frequent_itemsets = generate_frequent_itemsets(itemset_manager, min_support, max_length=max_length)
    
    # Calculate association rule statistics.
    for frequent_itemset in frequent_itemsets:
        rule_statistics = list(
            filter_rule_statistics(
                gen_rule_statistics(itemset_manager, frequent_itemset),
                min_confidence=min_confidence,
                min_lift=min_lift,
            )            
        )
        
        if not rule_statistics:
            continue
           
        rules_counter+=1
        if rules_counter>=max_rules:
            print('Maximum itemsets count limit reached!!!(' + str(max_rules) + ')')
            break
        
        yield Association_rule(frequent_itemset.items, frequent_itemset.support, frequent_itemset.count, rule_statistics)
