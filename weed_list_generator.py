import csv

noxweeds_csv = r'C:\projects\EDDMaps\weedlist.csv'

def process_csv(csvfile):
    """
    Converts a CSV file into a nicely formatted list of dictionaries, one for each line
    """

    # Note:
    # verify that the order of the columns is the same as below
    # 0=sub, 1=class, 2=name, 3=sciname
    # it may be different if you're getting it from 

    noxweeds_list = []

    with open(csvfile) as csvfile_raw:
        weeds = csv.reader(csvfile_raw)
        for row in weeds:
            weed = {'sub':row[0], 'class':row[1], 'name':row[2], 'sciname':row[3]}
            noxweeds_list.append(weed)
    
    noxweeds_list.pop(0) # remove the header line


    def sortweeds(weed):
        """
        sorting formatter function:
        returns a tuple, with the form (weed class, sub code)
        """
        return (weed['class'], int(weed['sub']))


    def prettify(weedlist):
        """
        Converts a list of dictionary objects into a nicely formatted string
        """
        noxweeds_str = "[\n"
        
        for x in weedlist:
            noxweeds_str = noxweeds_str + "    " + str(x) + ',\n'
        noxweeds_str = noxweeds_str + "]"
        return noxweeds_str

    noxweeds_list.sort(key=sortweeds)

    return(prettify(noxweeds_list))


noxweeds_string = process_csv(noxweeds_csv)

print(noxweeds_string)
