#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if len(fields) != 4:
        continue
    try:
        tenquan = fields[1]
        rating = float(fields[3])
        print(f"{tenquan}\t{rating}")
    except ValueError:
        continue
