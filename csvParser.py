import argparse
import sys, os
def read_broken_file(filepath,numOfColumns):
    ''' reads the broken file and returns an array containing rows,
     each row in an array of it's own. '''
    with open(filepath, 'r') as f1:
        content = f1.readlines()
    content = [x.rstrip() for x in content]
    rows=[]
    for _ in range(len(content)/numOfColumns):
        row=[]
        for i in range(numOfColumns):
            row.append(content.pop(0))
        rows.append(row)
    return rows

def get_usage():
    return '''Usage:  python csvParser.py <broken file filepath> <delimiter> <number of columns expected>'''

def csv_parser(filepath,d,numOfColumns):
    ''' Pure Python implementation '''
    rows = read_broken_file(filepath,numOfColumns)
    try:
        with open("output.csv",'w') as f2:
            for row in rows:
                f2.write(d.join(row)+'\n')
        return True
    except Exception:
        return False
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="the full path of the file we want to fix.")
    parser.add_argument("delimiter", help="the delimiter used in the broken file.")
    parser.add_argument("numOfColumns", help="number of columns that we expect to get out of the broken file.", type=int)
    args = parser.parse_args()
    
    ret = csv_parser(args.filepath,args.delimiter,args.numOfColumns)

    if ret:
        print "[#] Fixed broken file successfully!"
        print "[#] File saved to : {}{}".format(os.getcwd(),"\output.csv")
        print "[#] < ~ -      Goodbye     - ~ >"
    else:
        print "[!] Something went wrong..."
        print get_usage()
        print "[!] < ~ -      Exiting...     - ~ >"