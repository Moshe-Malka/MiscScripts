
import openpyxl
import sys
import re

filename = r"C:\Users\User\Desktop\data.xlsx"

# name = input("> Please type the name to extract: ")
# person = str(name).encode('UTF-8')
person = r"ערן פייגין".decode('UTF-8')
out_arr = []
try:
    wb = openpyxl.load_workbook(filename)
except Exception as e:
    print "Error reading file."
    sys.exit(1)
sheet_names = wb.get_sheet_names()
for sheet in sheet_names:
    current_sheet = wb.get_sheet_by_name(sheet)
    ##### get first row #####
    #TODO
    ##### get certain person's values according to the person's name #####
    for row in current_sheet.rows:
        if(row[1].value is not None):
            if(row[1].value == person):
                # getting the full row denoting the person's name
                # print list(row)[:1]+list(row)[2:]
                person_row = list(row)[:1]+list(row)[2:]
                for cell in person_row:
                    print cell.value
                # number_of_cols = len(list(row)[1:])
                # for i in range(number_of_cols):
                #     curr = list(row)[1:][i].value
                #     if(curr is not None):
                #         print curr
                        # out_arr.append(str(curr))   
    break
print out_arr
    # print sheet.encode('UTF-8')

