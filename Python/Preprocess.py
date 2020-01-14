###################################################################
# preprocessing section
###################################################################
def prepare_records(datasetName, datasetSep, datasetType, public, *args):

    global max_items

    if public==0:
        filepath=os.path.join('datasets', identity, str(datasetType), datasetName)
    else:
        filepath=os.path.join('public', str(datasetType), datasetName)

    if len(args)>max_items:
        print('Max column limit exceeded (' + str(max_items) + '). Only the first ' + str(max_items) + ' columns will be processed.')
        args=args[0:max_items+1]
    
    if datasetType==1:
        if len(args)==0:
            try:
                with open(filepath, mode='r') as f:
                    reader = csv.reader(f, delimiter=datasetSep)
                    return list(reader)
            except:
                print('Could not open or find dataset file!!!')
                return None

        else:
            try:           
                dataset = pd.read_csv(filepath, sep=datasetSep)
            except:
                return None
                
            #use only added columns
            if len(args)>1:
                dataset = dataset[list(args[1:])]
            #pandas to list
            records=dataset.values.tolist()
            #remove nan elements from this 2-dimensional list'
            records = [[y for y in x if str(y) != args[0]] for x in records]
            return(records)
            
    elif datasetType==2:
        try:
            dataset = pd.read_csv(filepath, sep=datasetSep)
        except:
            return None

        groupCol = args[0]
        itemsCol = args[1]

        dataset = dataset[[groupCol, itemsCol]]
        
        dataset.sort_values(by=groupCol)

        TempInv=''
        records=[]
        setrec=set()
        for index, row in dataset.iterrows():
            if TempInv!=row[groupCol]:
                if len(setrec)>1:
                    records.append(sorted(setrec))
                setrec=set()
                setrec.add(str(row[itemsCol]).strip())
                TempInv=row[groupCol]
            else:
                setrec.add(str(row[itemsCol]).strip())
                

        if len(setrec)>1:
            records.append(sorted(setrec))
            
        return(records)
                
    elif datasetType==3:
    
        try:
            dataset = pd.read_csv(filepath, sep=datasetSep)
        except:
            return None
        
        dataset = dataset[list(args[1:])]
        
        #put the name of product in item#
        for arg in args[1:]:
            dataset[arg]=[str(arg) if str(x)!=args[0] else args[0] for x in dataset[arg]]
        
        #pandas to list
        records=dataset.values.tolist()
        #remove nan elements from this 2-dimensional list'
        records = [[y for y in x if str(y) != args[0]] for x in records]
        return(records)
                            
    elif datasetType==4:
        if len(args)>0:
        
            try:
                dataset = pd.read_csv(filepath, sep=datasetSep)
            except:
                return None
                
            dataset = dataset[list(args)]
            
            for arg in args:
                dataset[arg] = arg + '=' + dataset[arg].astype(str)
            
            records=dataset.values.tolist()
            return(records)
            
        else:
            with open(filepath, mode='r') as f:
                try:
                    reader = csv.reader(f, delimiter=datasetSep)
                except:
                    return None
                    
                return list(reader)            
            
    else:
        print("Unknown dataset type")