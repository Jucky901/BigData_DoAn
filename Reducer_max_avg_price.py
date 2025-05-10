#!/usr/bin/env python3
import sys

current_id = None
total_price = 0.0
count = 0

for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')
    if len(parts) != 3:
        continue
    idquan, price_str, cnt_str = parts
    try:
        price = float(price_str)
        cnt = int(cnt_str)
    except ValueError:
        continue

    if current_id == idquan:
        total_price += price
        count += cnt
    else:
        if current_id is not None and count > 0:
            avg_price = total_price / count
            print(f"{current_id}\t{avg_price}")
        current_id = idquan
        total_price = price
        count = cnt

if current_id is not None and count > 0:
    avg_price = total_price / count
    print(f"{current_id}\t{avg_price}")
