import csv

array = []
call = 0
in_call = 0
sms = 0

with open('data.csv' , newline='') as File:
    reader = csv.reader(File)
    
    for row in reader:
        array.append(row)


for i in range(1,10):
    if '915642913' in array[i][1]:
        call+=float(array[i][3])
        sms+=float(array[i][4])
    if '915642913' in array[i][2]:
        in_call+=float(array[i][3])
        
call_value = (call+in_call)*1
if sms in range(5,10): sms_value = 5*0 + (sms-5)*1
elif sms > 10: sms_value = 5*0 + 5*1 + (sms-10)*2
else: sms_cost = 0
value = call_value + sms_value

print('Итого: {:.2f}'.format(value))
