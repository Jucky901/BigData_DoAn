#!/usr/bin/env python3
import sys

max_count = -1
max_quans = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    quan, count_str = line.split('|')
    try:
        count = int(count_str)
        if count > max_count:
            max_count = count
            max_quans = [quan]
        elif count == max_count:
            max_quans.append(quan)
    except ValueError:
        continue

for quan in max_quans:
    print(f"{quan}\t|\t{max_count}")

