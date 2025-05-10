#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')
    if len(parts) != 4:
        continue
    idquan, _, item, price = parts
    try:
        price = float(price)
        print(f"{idquan}\t{item}\t{price}")
    except ValueError:
        continue
