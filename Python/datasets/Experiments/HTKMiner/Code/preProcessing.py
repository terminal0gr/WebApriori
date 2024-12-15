import pandas

df1 = pandas.read_csv("chess.dat", sep=" ", header=None)

num_of_cols = len(df1.columns)#total num of columns.
num_of_rows = df1.count(axis=0)[0]# total num of rows.

#print(num_of_cols)
#print(num_of_rows)

trx = [str(i) for i in range(1, int(df1.max().max()) + 1)]#list containing values from 0 to max value in dataframe
#print(trx)
trxIds = []
d = dict.fromkeys(trx)#initialize dict with trx as keys and assign empty values.
row = df1.values.tolist()
for each in trx:
    i = 0;
    while(i != num_of_rows): #loop through every row for each iteration of trx.
        #current  = row[i]# i is the current row number, Var row contains complete row data.
        if float(each) in row[i]: #if value is present in current row.
            # if not d[each]: #if d[each] is currently empty
            #     d[each] = i # then assign row number to d[each]
            # else:
            #     d[each] = str(d[each]) + ", " + str(i)# get current value of d[each], add current row number to the value and assign back to d[each].
            trxIds.append(int(i))
            # print(trxIds)

        # else:
        # 	print(f"{each} not found in {i}")
        i +=1 #increment until total num of rows == i.
    d[each] = trxIds.copy()
    # d[each] = trxIds
    trxIds.clear()
    # d[each] = "["+str(d[each])+"]"
# print(d)

# print(row)
# data = d.items()# returns list of tuples in key, value pair.
# #print(ar)
# df2 = pandas.DataFrame(data, columns=["TrxID", "Trx"])
#
# # #print(data)
# df2.to_csv('transactions.csv')
#
# print(end - start)
#print(df2)
