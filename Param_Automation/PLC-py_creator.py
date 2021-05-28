from pprint import pprint
import xlrd
import json

#Format must be like this.
"""
{
            "from": "DailyPowerYields_5003_U16x04_11",
            "from_type": sdb.DT_UINT, 
            "from_count": 1,
            "to": "Telem_Invertor_11_Yields_DailyPower",
            "coeff": 10,
            "oper": "/",
            "samp_mode": "POLLING",
            "samp_rate": 60
            
}

"""


#we open the excel file which list of parameters in it
wb = xlrd.open_workbook("dataset.xlsx")

#Opening the related sheet
sheet = wb.sheet_by_index(2)

#List for JSON
shlist=[]

#Slave ID's are for making unique to all parameters
slavelist=[11,12,13,14,21,22,23,24,25]

#row numbers of excel file
rows = sheet.nrows

#temp list for manipulating a string parameter
temp=[]


def yaz(slave):

    for x in range(1, rows):

        temp = sheet.row_values(x)[0]
        temp = temp.split("_11_")
        mb_from = temp[0] + "_" + str(slave) + "_" + temp[1]

        from_type=sheet.row_values(x)[1]

        temp=sheet.row_values(x)[2]
        temp = temp.split("_11_")
        mqtt_to = temp[0] + "_" + str(slave) + "_" + temp[1]

        coeff = int(sheet.row_values(x)[3])



        msg = {
            "from": mb_from,
            "from_type": "?=sdb.DT_"+from_type+"&=?", #cfg file does not accept str, it must be: sdb.DT_UINT
            "from_count": 1,
            "to": mqtt_to,
            "coeff": coeff,
            "oper": "/",
            "samp_mode": "POLLING",
            "samp_rate": 60

                }

        shlist.append(msg)

#slave ID list FCT
for z in range(0, len(slavelist)):
    slave = slavelist[z]
    yaz(slave)


#pprint(shlist,indent=2)
#pprint(json.dumps(shlist))
print(json.dumps(shlist))
