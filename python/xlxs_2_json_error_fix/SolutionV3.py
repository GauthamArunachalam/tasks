import json
import xlrd

#Enter name of file here
workbook = xlrd.open_workbook('source.xlsx')
#Enter name of sheet here
worksheet = workbook.sheet_by_name('Sheet1')

data = []
keys = [v.value for v in worksheet.row(0)]



name_data = []
names = []
data2 = {}
row_data = {}
for row_number in range(worksheet.nrows):
    if row_number == 0:
        continue
    row_data = {}
    for col_number, cell in enumerate(worksheet.row(row_number)):
        if (keys[col_number] == 'name' and cell.value != "") or (col_number == 0 and cell.value!=""):
            data2['name'] = cell.value
        elif keys[col_number] == 'sortOrder' and cell.value !='' and col_number !=0 :
            b = int (cell.value)
            row_data[keys[col_number]] = b
            #print(row_data[keys[col_number]])
        elif keys[col_number] == 'isActive' and cell.value !='' and col_number != 0:
            if cell.value == 1:
                row_data[keys[col_number]] = True
            else:
               row_data[keys[col_number]] = False
        elif keys[col_number] != 'name' and col_number != 0:
            row_data[keys[col_number]] = cell.value
    if all(value == "" for value in row_data.values()):
        data2['surveyQuestions'] = name_data
        name_data = []
        data.append(data2)
        data2={}
    else:
        name_data.append(row_data)
data2['surveyQuestions'] = name_data
data.append(data2)
with open('output.json', 'w') as json_file:
    json_file.write(json.dumps({'sections': data}))