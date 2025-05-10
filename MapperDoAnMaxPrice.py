#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if len(fields) != 4:
        continue
    try:
        item = fields[2]
        price = int(fields[3])
        # Dùng price là key để sắp xếp dễ
        print(f"{item}\t{price}")
    except ValueError:
        continue
