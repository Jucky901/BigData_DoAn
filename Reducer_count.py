#!/usr/bin/env python3
import sys

current_id = None
count = 0

for line in sys.stdin:
    line = line.strip()
    idquan, value = line.split('\t')
    try:
        value = int(value)
    except ValueError:
        continue

    if current_id == idquan:
        count += value
    else:
        if current_id is not None:
            print(f"{current_id}\t{count}")
        current_id = idquan
        count = value

# output cuối cùng
if current_id is not None:
    print(f"{current_id}\t{count}")
