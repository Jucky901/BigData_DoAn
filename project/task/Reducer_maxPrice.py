#!/usr/bin/env python3
import sys

current_id = None
max_price = -1
max_item = ""

for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')
    if len(parts) != 3:
        continue
    idquan, item, price_str = parts
    try:
        price = float(price_str)
    except ValueError:
        continue

    if current_id == idquan:
        if price > max_price:
            max_price = price
            max_item = item
    else:
        if current_id is not None:
            print(f"{current_id}\t|\t{max_price}")
        current_id = idquan
        max_price = price
        max_item = item

# Output cuối cùng
if current_id is not None:
    print(f"{current_id}\t|\t{max_price}")

