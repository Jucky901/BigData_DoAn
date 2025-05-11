#!/usr/bin/env python3
import sys

max_id = None
max_avg = -1

for line in sys.stdin:
    line = line.strip()
    idquan, avg_str = line.split('|')
    try:
        avg = float(avg_str)
    except ValueError:
        continue

    if avg > max_avg:
        max_avg = avg
        max_id = idquan

if max_id is not None:
    print(f"{max_id}\t|\t{max_avg}")

