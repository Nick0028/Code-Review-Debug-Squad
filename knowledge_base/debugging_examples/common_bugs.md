# Common Python bugs
Off-by-one errors often occur when range(len(items) + 1) accesses one position beyond the list.
Check empty lists before dividing by their length. Validate inputs and test boundaries such as zero,
one item, negative values, empty strings and missing values.
