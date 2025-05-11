import json
import numpy as np
import pandas as pd

with open("datas/trademark_sample.json", "r", encoding="utf-8") as f:
    data = json.load(f)

lists = set()

for d in data:
    asign_codes = d.get('registrationDate', [])

    if isinstance(asign_codes, list):
        for code in asign_codes:
            if code is not None:
                try:
                    lists.add(code[:4])
                except ValueError:
                    continue
    else:
        if asign_codes is not None:
            try:
                lists.add(asign_codes[:4])
            except ValueError:
                continue

sorted_lists = sorted(lists, reverse=False)

print(sorted_lists)
