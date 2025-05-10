#!/usr/bin/env python3
import sys
import heapq

top_items = []

for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')
    if len(parts) != 2:
        continue
    try:
        item = parts[0]
        price = int(parts[1])
        heapq.heappush(top_items, (-price, item))
        if len(top_items) > 10:
            heapq.heappop(top_items)
    except ValueError:
        continue

for neg_price, item in sorted(top_items, reverse=True):
    print(f"{item}\t{-neg_price}")
