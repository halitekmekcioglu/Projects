
from pprint import pprint
import xlrd
import json

#Format must be like this.
"""
     {
                    "index": 0, 
                    "enable": true, 
                    "slave": 12, 
                    "interval": 1, 
                    "sort_index": 581, 
                    "fcode": 4, 
                    "length": 1, 
                    "byte_format": "AB", 
                    "tagname": "String1Current_7013_U16x04_12", 
                    "type": "UINT", 
                    "register": 7012
                }, 
"""

#we open the excel file which list of parameters in it
wb = xlrd.open_workbook("dataset.xlsx")

#Opening the sheet
sheet = wb.sheet_by_index(0)

#List for JSON
shlist=[]

#Slave ID's are for making unique to all parameters
slavelist=[11,12,13,14,21,22,23,24,25]

#row numbers of excel file
rows = sheet.nrows

#temp list for manipulating a string parameter
tagnamel=[]


def yaz(slave):

    for x in range(1, rows):

        index=int(sheet.row_values(x)[0])
        enable=bool(sheet.row_values(x)[1])
        interval=int(sheet.row_values(x)[3])
        sort_index=int(sheet.row_values(x)[4])
        fcode=int(sheet.row_values(x)[5])
        length=int(sheet.row_values(x)[6])
        byte_format=sheet.row_values(x)[7]

        tagnamel=sheet.row_values(x)[8]
        tagnamel=tagnamel.split("_")
        tagname=tagnamel[0]+"_"+str(slave)+"_"+tagnamel[2]+"_"+tagnamel[3]

        types=sheet.row_values(x)[9]
        regs=int(sheet.row_values(x)[10])

        msg = {
            "index": index,
            "enable": enable,
            "slave": slave,
            "interval": interval,
            "sort_index": sort_index,
            "fcode": fcode,
            "length": length,
            "byte_format": byte_format,
            "tagname": tagname,
            "type": types,
            "register": regs
        }
        shlist.append(msg)

#slave ID list FCT
for z in range(0, len(slavelist)):
    slave = slavelist[z]

    yaz(slave)

#sort_index adding
for si in range(0, ((rows-1) * len(slavelist))):
    shlist[si]["sort_index"]=si

#pprint(shlist,indent=2)
print(json.dumps(shlist))

