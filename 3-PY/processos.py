import csv, re, json
db = []

#Normalize :: double colon separated values into nested list
with open("./sources/processos.txt", encoding="utf-8") as file:
    for line in file:
        db.append(line.strip().split('::'))

print(db)

