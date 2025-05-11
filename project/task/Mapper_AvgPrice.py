#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if len(fields) != 4:
        continue
    try:
        idquan = fields[0]
        price = float(fields[3])
        print(f"{idquan}\t{price}\t1")
    except ValueError:
        continue

