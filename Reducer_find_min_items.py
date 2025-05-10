#!/usr/bin/env python3
import sys

min_count = None
min_quans = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    quan, count_str = line.split()
    try:
        count = int(count_str)
        if min_count is None or count < min_count:
            min_count = count
            min_quans = [quan]
        elif count == min_count:
            min_quans.append(quan)
    except ValueError:
        continue

for quan in min_quans:
    print(f"{quan}\t{min_count}")
