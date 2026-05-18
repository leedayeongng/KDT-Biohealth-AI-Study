import csv
data_list = []
with open('paxnet.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='|')
    for row in reader:
        data_list.append(row)
print(data_list)
for v in data_list:
    print(v[0])