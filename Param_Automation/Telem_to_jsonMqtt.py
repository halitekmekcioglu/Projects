from pprint import pprint
import xlrd
import json

#Format must be like this.
"""
{
            "unitMultiplicator": "1", 
            "name": "Telem_Invertor_25_Fault_TimeDay", 
            "cb": {
                "addreq": "CLEAR"
            }, 
            "invertSign": "0", 
            "alias": "Telem.CAP9.Invertor_25_Fault_TimeDay", 
            "mode": {
                "qual": "QUAL", 
                "addreq": "LOGGER", 
                "val": "CACHE"
            }, 
            "type": "teledot", 
            "sampleRate": "PT15S", 
            "pointType": "Unknown", 
            "evt": {
                "addreq": "SET"
            }, 
            "unit": ""
        }
"""


#we open the excel file which list of parameters in it
wb = xlrd.open_workbook("dataset.xlsx")

#Opening the related sheet
sheet = wb.sheet_by_index(1)

#List for JSON
shlist=[]

#Slave ID's are for making unique to all parameters
slavelist=[11,12,13,14,21,22,23,24,25]

#CAP numbers
CAPlist=[1,2,3,4,5,6,7,8,9]

#row numbers of excel file
rows = sheet.nrows

#temp list for manipulating a string parameter
temp=[]


def yaz(slave,CAPno):

    for x in range(1, rows):

        temp=sheet.row_values(x)[0]
        temp = temp.split("_11_")
        name = temp[0] + "_" + str(slave) + "_" + temp[1]

        temp=sheet.row_values(x)[1]
        temp=temp.split("CAP1")
        temp=temp[0]+"CAP"+str(CAPno)+temp[1]
        temp = temp.split("_11_")
        alias = temp[0] + "_" + str(slave)+"_"+ temp[1]


        msg = {
            "unitMultiplicator": "1",
            "name": name,
            "cb": {
                "addreq": "CLEAR"
                    },
            "invertSign": "0",
            "alias": alias,
            "mode": {
                "qual": "QUAL",
                "addreq": "LOGGER",
                "val": "CACHE"
                    },
            "type": "teledot",
            "sampleRate": "PT15S",
            "pointType": "Unknown",
            "evt": {
                "addreq": "SET"
                        },
            "unit": ""
            }

        shlist.append(msg)

#slave ID list FCT
for z in range(0, len(slavelist)):
    slave = slavelist[z]
    CAPno=CAPlist[z]
    yaz(slave,CAPno)


#pprint(shlist,indent=2)
#pprint(json.dumps(shlist))
print(json.dumps(shlist))
