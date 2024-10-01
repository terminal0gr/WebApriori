
"""
csv.py - read/write/investigate CSV files
"""

import re
from _csv import Error, __version__, writer, reader, register_dialect, \
                 unregister_dialect, get_dialect, list_dialects, \
                 field_size_limit, \
                 QUOTE_MINIMAL, QUOTE_ALL, QUOTE_NONNUMERIC, QUOTE_NONE, \
                 __doc__
from _csv import Dialect as _Dialect

from collections import OrderedDict
from io import StringIO

# Malliaridis 20240829 Created to subtistude the original regex in def _guess_quote_and_delimiter which is not working always right
def is_double_quoted(data, delimiter=',', quotechar='"'):
    # Split the string into lines
    lines = data.splitlines()

    # Loop over each line in the string
    for line in lines:
        in_quotes = False  # Flag to check if we are inside quotes
        for char in line:
            if char == quotechar:
                in_quotes = not in_quotes  # Toggle the in_quotes flag
        if in_quotes:
            return False  # If still in quotes by the end of the line, it's improperly quoted
    return True  # If no issues were found, the string is properly quoted

__all__ = ["QUOTE_MINIMAL", "QUOTE_ALL", "QUOTE_NONNUMERIC", "QUOTE_NONE",
           "Error", "Dialect", "__doc__", "excel", "excel_tab",
           "field_size_limit", "reader", "writer",
           "register_dialect", "get_dialect", "list_dialects", "Sniffer",
           "unregister_dialect", "__version__", "DictReader", "DictWriter",
           "unix_dialect"]

class Dialect:
    """Describe a CSV dialect.

    This must be subclassed (see csv.excel).  Valid attributes are:
    delimiter, quotechar, escapechar, doublequote, skipinitialspace,
    lineterminator, quoting.

    """
    _name = ""
    _valid = False
    # placeholders
    delimiter = None
    quotechar = None
    escapechar = None
    doublequote = None
    skipinitialspace = None
    lineterminator = None
    quoting = None
    datasetType = 0 # 0:Unspecified, 1:Market Basket List
    header=None

    def __init__(self):
        if self.__class__ != Dialect:
            self._valid = True
        self._validate()

    def _validate(self):
        try:
            _Dialect(self)
        except TypeError as e:
            # We do this for compatibility with py2.3
            raise Error(str(e))

class excel(Dialect):
    """Describe the usual properties of Excel-generated CSV files."""
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL
register_dialect("excel", excel)

class excel_tab(excel):
    """Describe the usual properties of Excel-generated TAB-delimited files."""
    delimiter = '\t'
register_dialect("excel-tab", excel_tab)

class unix_dialect(Dialect):
    """Describe the usual properties of Unix-generated CSV files."""
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\n'
    quoting = QUOTE_ALL
register_dialect("unix", unix_dialect)


class DictReader:
    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect="excel", *args, **kwds):
        self._fieldnames = fieldnames   # list of keys for the dict
        self.restkey = restkey          # key to catch long rows
        self.restval = restval          # default value for short rows
        self.reader = reader(f, dialect, *args, **kwds)
        self.dialect = dialect
        self.line_num = 0

    def __iter__(self):
        return self

    @property
    def fieldnames(self):
        if self._fieldnames is None:
            try:
                self._fieldnames = next(self.reader)
            except StopIteration:
                pass
        self.line_num = self.reader.line_num
        return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, value):
        self._fieldnames = value

    def __next__(self):
        if self.line_num == 0:
            # Used only for its side effect.
            self.fieldnames
        row = next(self.reader)
        self.line_num = self.reader.line_num

        # unlike the basic reader, we prefer not to return blanks,
        # because we will typically wind up with a dict full of None
        # values
        while row == []:
            row = next(self.reader)
        d = OrderedDict(zip(self.fieldnames, row))
        lf = len(self.fieldnames)
        lr = len(row)
        if lf < lr:
            d[self.restkey] = row[lf:]
        elif lf > lr:
            for key in self.fieldnames[lr:]:
                d[key] = self.restval
        return d


class DictWriter:
    def __init__(self, f, fieldnames, restval="", extrasaction="raise",
                 dialect="excel", *args, **kwds):
        self.fieldnames = fieldnames    # list of keys for the dict
        self.restval = restval          # for writing short dicts
        if extrasaction.lower() not in ("raise", "ignore"):
            raise ValueError("extrasaction (%s) must be 'raise' or 'ignore'"
                             % extrasaction)
        self.extrasaction = extrasaction
        self.writer = writer(f, dialect, *args, **kwds)

    def writeheader(self):
        header = dict(zip(self.fieldnames, self.fieldnames))
        self.writerow(header)

    def _dict_to_list(self, rowdict):
        if self.extrasaction == "raise":
            wrong_fields = rowdict.keys() - self.fieldnames
            if wrong_fields:
                raise ValueError("dict contains fields not in fieldnames: "
                                 + ", ".join([repr(x) for x in wrong_fields]))
        return (rowdict.get(key, self.restval) for key in self.fieldnames)

    def writerow(self, rowdict):
        return self.writer.writerow(self._dict_to_list(rowdict))

    def writerows(self, rowdicts):
        return self.writer.writerows(map(self._dict_to_list, rowdicts))

# Guard Sniffer's type checking against builds that exclude complex()
try:
    complex
except NameError:
    complex = float

class Sniffer:
    '''
    "Sniffs" the format of a CSV file (i.e. delimiter, quotechar)
    Returns a Dialect object.
    '''
    def __init__(self):
        # in case there is more than one possible delimiter
        # Malliaridis 20231209 changed preferred character order, because in some countries ',' is used as decimal separator
        # leadding to wrong delimiter detection. 
        self.preferred = [';', ',', '\t', ':']
        #self.preferred = [',', '\t', ';', ' ', ':']


    def sniff(self, sample, delimiters=None):
        """
        Returns a dialect (or None) corresponding to the sample
        """

        quotechar, doublequote, delimiter, skipinitialspace = self._guess_quote_and_delimiter(sample, delimiters)

        #Malliaridis 28/08/2024 We want to know if there is quotechar in self._guess_delimiter
        #                       because when we count the frequency of a character in a line 
        #                       we want to exclude the character from counting if it is inside quotation marks.
        # e.g.    a,b,"ab,cd,ed,a",c,d we want to return count=4
        quoteCh=None
        if quotechar!='' and doublequote:
            quoteCh=quotechar

        if not delimiter:
            delimiter, skipinitialspace, datasetType = self._guess_delimiter(sample, delimiters, quoteCh)
        else: #Malliaridis 23/12/2023
            # we use _guess_delimiter only for examine if it is dataset of type 1-MBL - Market Basket list.
            # This is neseccary because that kind of dataset has indistinct number of columns in each line
            # making easy to be detected without engaging the ML detection that follows in other dataset types.
            delimiter1, temp_skipinitialspace, datasetType = self._guess_delimiter(sample, delimiters, quoteCh)
            if delimiter1:
                if delimiter1 in self.preferred:
                    delimiter=delimiter1

        if not delimiter:
            raise Error("Could not determine delimiter")

        class dialect(Dialect):
            _name = "sniffed"
            lineterminator = '\r\n'
            quoting = QUOTE_MINIMAL
            # escapechar = ''

        dialect.doublequote = doublequote
        dialect.delimiter = delimiter
        # _csv.reader won't accept a quotechar of ''
        dialect.quotechar = quotechar or '"'
        dialect.skipinitialspace = skipinitialspace
        dialect.datasetType = datasetType

        return dialect

    def _guess_quote_and_delimiter(self, data, delimiters):
        """
        Looks for text enclosed between two identical quotes
        (the probable quotechar) which are preceded and followed
        by the same character (the probable delimiter).
        For example:
                         ,'some text',
        The quote with the most wins, same with the delimiter.

        #Malliaridis 08/07/2024 The number of matches found must be at least 90% of the number of rows in sample.
        #e.g. if sample rows are 500, then matches found must be at least 450. 
        #Note that the number of matches could be greater than rows (e.g.+500 matches for 500 rows) if more than one quoted string exists in a row

        If there is no quotechar the delimiter can't be determined
        this way.
        """

        dataRowsCount = len(list(filter(None, data.split('\n'))))

        matches = []
        #Malliaridis 25/08/2024
        #Some dataset have ,"abc", but also ,"ab ""c"" d", case which confuses the compiler. the 5~8 regex do solve this problem.
        for restr in (r'(?P<delim>[^\w\n"\'])(?P<space> ?)(?P<quote>["\']).*?(?P=quote)(?P=delim)',           # ,".*?",
                      r'(?:^|\n)(?P<quote>["\']).*?(?P=quote)(?P<delim>[^\w\n"\'])(?P<space> ?)',             #  ".*?",
                      r'(?P<delim>[^\w\n"\'])(?P<space> ?)(?P<quote>["\']).*?(?P=quote)(?:$|\n)',             # ,".*?"
                      r'(?:^|\n)(?P<quote>["\']).*?(?P=quote)(?:$|\n)',                                       #  ".*?" (no delim, no space)
                      r'(?P<delim>[^\w\n"\'])(?P<space> ?)(?P<quote>["\'])(?:(?!\3).)+?(?P=quote)(?P=delim)', # ,".*?", excluding "" or '' case
                     ):    
        #Original...         
        # for restr in (r'(?P<delim>[^\w\n"\'])(?P<space> ?)(?P<quote>["\']).*?(?P=quote)(?P=delim)', # ,".*?",
        #               r'(?:^|\n)(?P<quote>["\']).*?(?P=quote)(?P<delim>[^\w\n"\'])(?P<space> ?)',   #  ".*?",
        #               r'(?P<delim>[^\w\n"\'])(?P<space> ?)(?P<quote>["\']).*?(?P=quote)(?:$|\n)',   # ,".*?"
        #               r'(?:^|\n)(?P<quote>["\']).*?(?P=quote)(?:$|\n)'):                            #  ".*?" (no delim, no space)
            regexp = re.compile(restr, re.DOTALL | re.MULTILINE)
            matches = regexp.findall(data)
            if len(matches)>=dataRowsCount*0.9:
            #original...
            #if matches:
                break

        # If no matches found corresponding to the regex above -> no quotechar and delimitel is not detected.
        if not matches:
            return ('', False, None, 0)
        
        # If matches found but less than the thresohold below corresponding to the regex above -> no quotechar and delimitel is not detected.
        #if len(matches)<dataRowsCount*0.9:
        #   return ('', False, None, 0)

        quotes = {}
        delims = {}
        spaces = 0
        groupindex = regexp.groupindex
        for m in matches:
            n = groupindex['quote'] - 1
            key = m[n]
            if key:
                quotes[key] = quotes.get(key, 0) + 1
            try:
                n = groupindex['delim'] - 1
                key = m[n]
            except KeyError:
                continue
            if key and (delimiters is None or key in delimiters):
                delims[key] = delims.get(key, 0) + 1
            try:
                n = groupindex['space'] - 1
            except KeyError:
                continue
            if m[n]:
                spaces += 1

        quotechar = max(quotes, key=quotes.get)

        if delims:
            delim = max(delims, key=delims.get)
            skipinitialspace = delims[delim] == spaces
            if delim == '\n': # most likely a file with a single column
                delim = ''
        else:
            # there is *no* delimiter, it's a single column of quoted data
            delim = ''
            skipinitialspace = 0

        # if we see an extra quote between delimiters, we've got a
        # double quoted format
        # Malliaridis 20240829 Created to subtistude the original regex below which is not working always right
        doublequote = is_double_quoted(data, delim, quotechar)
        # dq_regexp = re.compile(
        #                        r"((%(delim)s)|^)\W*%(quote)s[^%(delim)s\n]*%(quote)s[^%(delim)s\n]*%(quote)s\W*((%(delim)s)|$)" % \
        #                        {'delim':re.escape(delim), 'quote':quotechar}, re.MULTILINE)
        # if dq_regexp.search(data):
        #     doublequote = True
        # else:
        #     doublequote = False

        return (quotechar, doublequote, delim, skipinitialspace)


    def     _guess_delimiter(self, data, delimiters, quoteChar=None):
        """
        The delimiter /should/ occur the same number of times on
        each row. However, due to malformed data, it may not. We don't want
        an all or nothing approach, so we allow for small variations in this
        number.
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
        """

        data = list(filter(None, data.split('\n')))

        ascii = [chr(c) for c in range(127)] # 7-bit ASCII
        

        # build frequency tables
        chunkLength = min(10, len(data))
        iteration = 0
        charFrequency = {}
        modes = {}
        delims = {}
        start, end = 0, chunkLength
        while start < len(data):
            iteration += 1
            for line in data[start:end]:
                for char in ascii:
                    metaFrequency = charFrequency.get(char, {})
                    # must count even if frequency is 0

                    #Malliaridis 27/08/2024
                    #original freq = line.count(char) 
                    if quoteChar is None:
                        freq = line.count(char)
                    else:
                        # Count manually because we want to exclude character counting if is in quotation Marks
                        freq=0
                        inside_quotes = False
                        for ch in line:
                            if ch == quoteChar:
                                # Toggle the inside_quotes flag whenever a quote is encountered
                                inside_quotes = not inside_quotes
                            elif ch == char and not inside_quotes:
                                # Count the comma if we are not inside quotes
                                freq+=1

                    # value is the mode
                    metaFrequency[freq] = metaFrequency.get(freq, 0) + 1
                    charFrequency[char] = metaFrequency 

            for char in charFrequency.keys():
                items = list(charFrequency[char].items())
                if len(items) == 1 and items[0][0] == 0:
                    continue
                # get the mode of the frequencies
                if len(items) > 1:
                    modes[char] = max(items, key=lambda x: x[1])
                    # adjust the mode - subtract the sum of all
                    # other frequencies
                    items.remove(modes[char])
                    modes[char] = (modes[char][0], modes[char][1]
                                   - sum(item[1] for item in items))
                else:
                    modes[char] = items[0]

            # build a list of possible delimiters
            modeList = modes.items()
            total = float(min(chunkLength * iteration, len(data)))
            # (rows of consistent data) / (number of rows) = 100%
            consistency = 1.0
            # minimum consistency threshold
            threshold = 0.85
            while len(delims) == 0 and consistency >= threshold:
                for k, v in modeList:
                    if v[0] > 0 and v[1] > 0:
                        if ((v[1]/total) >= consistency and
                            (delimiters is None or k in delimiters)):
                            delims[k] = v
                consistency -= 0.01

            # Malliaridis 20240825
            if len(delims) > 0:
                # Malliaridis 20231209  
                # if there's more than one, fall back to a 'preferred' list
                # However, for better detection, the dict is beeing sorted by the highest frequency character
                    
                # Sort the list by the first item of each tuple in descending order
                sortDelimsByMaxFrequency = dict(sorted(delims.items(), key=lambda item: item[1][0], reverse=True))
                for item in sortDelimsByMaxFrequency:
                    if item[0] in self.preferred:
                        #Match! return it!
                        skipinitialspace = (data[0].count(item[0]) ==
                                            data[0].count("%c " % item[0]))             
                        return (item[0], skipinitialspace, 0)  

                #None of the characters in the dataset's delimiter candidates is in preferred list
                #OoooK! return the most frequent even if is not in the list of preferred delimiters
                for item in sortDelimsByMaxFrequency:
                    skipinitialspace = (data[0].count(item[0]) ==
                                        data[0].count("%c " % item[0]))             
                    return (item[0], skipinitialspace, 0)  
                # skipinitialspace = (data[0].count(sortDelimsByMaxFrequency[0][0]) ==
                #                     data[0].count("%c " % sortDelimsByMaxFrequency[0][0]))             
                # return (sortDelimsByMaxFrequency[0][0], skipinitialspace, 0)                

            #Original code
            # if len(delims) == 1:
            #     delim = list(delims.keys())[0]
            #     skipinitialspace = (data[0].count(delim) ==
            #                         data[0].count("%c " % delim))
            #     return (delim, skipinitialspace, 0)

            # analyze another chunkLength lines
            start = end
            end += chunkLength

        if not delims:
            
            #Malliaridis 03/12/2023 start
            #Dataset Type 1

            possibles = "|¦,; \t"  # \t represents Tab

            min_count = 0
            result = None

            for char in possibles:
                count=0
                for line in data:
                    pieces = line.split(char)
                    count += len(pieces)-1
                # pieces = data[0].split(char)
                # count = len(pieces)

                if min_count < count:
                    min_count = count
                    result=char

            return (result, 0, 1)
            #Malliaridis 03/12/2023 end
            #Malliaridis 03/12/2023 replaced
            #return('',0)
                    

        # Malliaridis 20240121. Replaced original lines
        # Delimiter could not be detected.
        return(None, None, 0)
        # Malliaridis 20240121. Replaced original lines
        # nothing else indicates a preference, pick the character that
        # dominates(?)
        # items = [(v,k) for (k,v) in delims.items()]
        # items.sort()
        # delim = items[-1][1]

    def has_header(self, sample, forceDelimiter=None, forceHasHeader=None):
        # Creates a dictionary of types of data in each column. If any
        # column is of a single type (say, integers), *except* for the first
        # row, then the first row is presumed to be labels. If the type
        # can't be determined, it is assumed to be a string in which case
        # the length of the string is the determining factor: if all of the
        # rows except for the first are the same length, it's a header.
        # Finally, a 'vote' is taken at the end for each column, adding or
        # subtracting from the likelihood of the first row being a header.

        dialect = self.sniff(sample)

        # Update mode. Delimiter has changed from user or other reason and must be managed
        if forceDelimiter!=None:
            dialect.delimiter=forceDelimiter

        # Update mode. Delimiter has changed from user or other reason and must be managed
        if forceHasHeader==False:
            return (False, None, dialect)

        rdr = reader(StringIO(sample), dialect)
        header = next(rdr) # assume first row is header

        columns = len(header)
        columnTypes = {}
        for i in range(columns): columnTypes[i] = None

        checked = 0
        #Malliaridis 03/12/2023 start
        rowsWithDifferentNumberOfColumnsFromFirstRowColumns=0
        headerItemFound=0
        for row in rdr:
            # arbitrary number of rows to check, to keep it sane
            if checked > 100:
                break
            checked += 1

            if len(row) != columns:
                rowsWithDifferentNumberOfColumnsFromFirstRowColumns+=1
                continue # skip rows that have irregular number of columns

            for col in list(columnTypes.keys()):

                for thisType in [int, float, complex]:
                    try:
                        thisType(row[col])
                        break
                    except (ValueError, OverflowError):
                        pass
                else:
                    # fallback to length of string
                    thisType = len(row[col])

                if thisType != columnTypes[col]:
                    if columnTypes[col] is None: # add new column type
                        columnTypes[col] = thisType
                    else:
                        # type is inconsistent, remove column from
                        # consideration
                        del columnTypes[col]

                #enumerate the items from header that match the items from the next # lines
                if header[col]==row[col]:
                    headerItemFound+=1

        #checked is the lines from the sample dataset without the header.
        if checked>0:
            #if the dataset is of the type 1) Market Basket list then it must not have a header.
            #if the ratio of lines with different number of columns from header is more than 0.2 then we assume we have an 1) Market Basket list
            if rowsWithDifferentNumberOfColumnsFromFirstRowColumns/checked>0.2:
                if forceHasHeader is None:
                    # normal case
                    return (False, None, dialect)
                else:
                    # Forced by user case
                    return (forceHasHeader, None, dialect)
            
        #If not even one item from the header found in the next # lines then it is propably header!
        if headerItemFound==0:
            if forceHasHeader is None:
                # normal case
                return (True, header, dialect)
            else:
                # Forced by user case
                return (forceHasHeader, None, dialect)
            
        #Malliaridis 03/12/2023 end

        # finally, compare results against first row and "vote"
        # on whether it's a header
        hasHeader = 0
        for col, colType in columnTypes.items():
            if type(colType) == type(0): # it's a length
                if len(header[col]) != colType:
                    hasHeader += 1
                else:
                    hasHeader -= 1
            else: # attempt typecast
                try:
                    colType(header[col])
                except (ValueError, TypeError):
                    hasHeader += 1
                else:
                    hasHeader -= 1

        if forceHasHeader is None:
            if hasHeader > 0:
                return (True, header, dialect)
            else:
                return (False, None, dialect)
        else:
            if forceHasHeader:
                return (True, header, dialect)
            else:
                return (False, None, dialect)

