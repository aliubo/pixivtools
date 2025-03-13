from typing import Sequence

def get_unique_ids(ids: Sequence[int]) -> list[int]:
    records = set()
    res = []
    for i in ids:
        if i not in records:
            records.add(i)
            res.append(i)
    return res
