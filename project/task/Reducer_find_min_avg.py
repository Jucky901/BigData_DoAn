#!/usr/bin/env python3
import sys

min_avg = float('inf')
min_quan = ""

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    quan, avg_str = line.split('|')
    try:
        avg = float(avg_str)
        if avg < min_avg:
            min_avg = avg
            min_quan = quan
    except ValueError:
        continue

print(f"{min_quan}\t|\t{min_avg}")

