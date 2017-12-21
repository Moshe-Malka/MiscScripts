
import sys
import re

def getWB(filename):
    try:
        return openpyxl.load_workbook(filename)
    except Exception:
        print "Error reading file."
        print "File path : {0}".format(filename)
        sys.exit(1)

def getSheetHeader(sh):
    head = []
    for i in range(1,len(list(sh.columns))+1):
        val = sh.cell(row=1, column=i).value
        if(val is not None):
            head.append(val)
    head = head[:1]+head[2:]
    return head

def getValuesByName(person, sheet):
    values = []
    for row in sheet.rows:
        if(row[1].value is not None):
            if(row[1].value == person):
                person_row = list(row)[:1]+list(row)[2:]
                for cell in person_row:
                    if (cell.value is not None):
                        values.append(cell.value)
    return values

def matchArrays(a, b):
    return map(None, a, b)

if __name__ == '__main__':
    try:
        import openpyxl
    except ImportError as e:
        print "[!] Please install openpyxl before running this script."
        print "pip install openpyxl"

    # filename = r"C:\Users\User\Desktop\data.xlsx"
    filename = "/Users/moshemalka/Desktop/data.xlsx"

    # getting our main openpyxl obj.
    wb = getWB(filename)

    # name = input("> Please type the name to extract: ")
    # person = str(name).encode('UTF-8')
    person = r"ערן פייגין".decode('UTF-8')
    matched_arr = []

    sheet_names = wb.get_sheet_names()
    for sheet in sheet_names:
        c_data = []
        current_sheet = wb.get_sheet_by_name(sheet)
        header = getSheetHeader(current_sheet)
        row_values = getValuesByName(person, current_sheet)
        ##TODO: make a function that takes 2 args - sheet name and values (sheet, matched_arr), and prints them out.
        print "*************" + sheet + "*************"
        matched_arr.append(matchArrays(header, row_values))
        # break
    # print out_arr
    for x in matched_arr:
        for y in x:
            for z in x:
                print z[0]
                print z[1]
                print "["+"-"*50+"]"
        
