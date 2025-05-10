#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if len(fields) != 4:
        continue
    idquan = fields[0]
    print(f"{idquan}\t1")
