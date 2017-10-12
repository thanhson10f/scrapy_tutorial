import json
import csv

content = ''
with open('unknown.jl', 'r') as f:
    content = f.readlines()

with open('found_name.csv', 'wt') as f:
    writer = csv.writer(f)
    for line in content:
        obj = json.loads(line)
        if obj['product_name']:
            writer.writerow((obj['gtin_code'], obj['product_name'].encode('utf-8').strip()))
            print(obj['gtin_code']+","+obj['product_name'])
