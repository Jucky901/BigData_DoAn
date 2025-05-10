#!/usr/bin/env python3
import sys
import heapq

top_quans = []

for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')
    if len(parts) != 2:
        continue
    try:
        tenquan = parts[0]
        rating = float(parts[1])
        heapq.heappush(top_quans, (rating, tenquan))
        if len(top_quans) > 10:
            heapq.heappop(top_quans)
    except ValueError:
        continue

for rating, tenquan in sorted(top_quans, reverse=True):
    print(f"{tenquan}\t{rating}")
