rem arguments:
rem 1 -> dataset name. Must be found in ../dataset file
rem 2 -> K parameter for the TopK frequent pattern mining
rem 3 -> item separation/delimiter in each dataset transaction
rem 4 -> Memory Save mode. If True, more efficient memory use but a little slower runtime
rem 5 -> runtimeThreshold in seconds (CommitTimeout)

call python HTKnegFINTest.py "webdocs.dat" "100" " " "False" "10000"


pause
pause
