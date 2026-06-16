Eclat
-----

This software is an implementation of the Eclat algorithm by Bart Goethals.
It uses the vertical database layout to compute all frequent itemsets with
support threshold above the given minimal support.


USAGE:
======

Eclat is invoked with two <mandatory> and one [optional] parameter:

./eclat <datafile> <minsup> [output]

- datafile: single text file containing the dataset in supermarket format. Items
            must have integers as IDs,
- minsup: specifies the minimal support of itemsets (i.e. the absolute value),
- output: optional parameter specifying the name of the outputfile.

