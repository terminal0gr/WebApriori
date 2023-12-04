AutoML Delimiter detection

   If the detaset is of type
      1) Market Basket list
   then the delimiter won't occur the same number of times on each row. In that case the delimiter 
   is the most frequent char in the sample (first 100 lines) between |¦,; and [tab]
   Moreover, If the dataset is 1) Market Basket list, then it has no header line.

   On the contrary, the delimiter /should/ occur the same number of times on
   each row if the dataset is of the type: 
      2) Order/Invoice detail
      3) Sparse item Dataset
      4) Columns with multiple categorized values
   However, due to malformed data, it may not. We don't want
   an all or nothing approach, so we allow for small variations in this
   number.
   On the other hand if the detaset is of type
      1) Market Basket list
   then the delimiter won't occur the same number of times on each row. In that case the delimiter 
   is the most frequent char in the sample (first 100 lines)

      1) build a table of the frequency of each character on every line.
      2) build a table of frequencies of this frequency (meta-frequency?),
         e.g.  'x occurred 5 times in 10 rows, 6 times in 1000 rows,
         7 times in 2 rows'
      3) use the mode of the meta-frequency to determine the /expected/
         frequency for that character
      4) find out how often the character actually meets that goal
      5) the character that best meets its goal is the delimiter
   For performance reasons, the data is evaluated in chunks, so it can
   try and evaluate the smallest portion of the data possible, evaluating
   additional chunks as necessary.