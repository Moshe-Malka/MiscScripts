# -*- coding: utf-8 -*-

import sys
import re

def getWorkBook(fname):
    try:
        return openpyxl.load_workbook(fname)
    except IOError:
        print "Error reading file."
        print "File path : {0}".format(filename)
        sys.exit(1)

def getSheetHeaders(sh):
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

def pprintResults(sheetName, values):
    print '[------------' + sheetName + '------------]\n'
    for val in values:
        if None not in val:
            if type(val[1]) is float:
                print val[0] + " : " 
                print str(val[1]).replace(".","")
            else:
                print val[0] + " : "
                print val[1]
        else:
            print val[0] + " : -"

def writeTofile(m_person, shName, m_values):
    with open('output.txt', 'wb') as writer:
        writer.write(m_person.encode('utf-8'))
        writer.write(shName.encode('utf-8') + '\n')
        data = []
        for val in m_values:
            if None not in val:
                if type(val[1]) is float:
                    data.append(val[0] + " : ")
                    data.append(str(val[1]).replace(".",""))
                else:
                    data.append(val[0] + " : ")
                    data.append(val[1])
            else:
                data.append(val[0] + " : -")
        data = [x.encode('utf-8') for x in data]
        writer.writelines(data)

if __name__ == '__main__':
    try:
        import openpyxl
    except ImportError as e:
        print "[!] Please install openpyxl before running this script."
        print "pip install openpyxl"

    # name = input("> Please type the name to extract: ")
    # person = name.encode('UTF-8')
    person = r"ערן פייגין".encode('UTF-8')
    filename = "/Users/moshemalka/Desktop/data.xlsx"

    wb = getWorkBook(filename)

    sheet_names = wb.get_sheet_names()
    print "Results for : {}".format(person.encode('UTF-8'))
    for sheet in sheet_names:
        current_sheet = wb.get_sheet_by_name(sheet)
        headers = getSheetHeaders(current_sheet)
        row_values = getValuesByName(person, current_sheet)
        pprintResults(sheet, matchArrays(headers, row_values))
        # writeTofile(person, sheet, matchArrays(headers, row_values))
        print "\n"
        
# fixed 2 errors in the xslx file:
#   in the fax2mail sheet - the name column should be B. as in all other sheets.
#   i fixed it by moved the name column to the B section.
#   i also fixed it in some more sheets.
#
#   in the phones column - for some reason it skips the empty value and mixes up the headers 
#   with the values. i fixed it by simply adding the same value to the remaning cells.
#