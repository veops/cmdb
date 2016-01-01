import os
from collections import defaultdict

d = defaultdict(int) # value is 'int'

for dirpath, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if dirpath.endswith("tools"):
            continue
        path = os.path.join(dirpath, filename)
        ext = os.path.splitext(filename)[1]
        d[ext] += len(list(open(path)))

for ext, n_lines in d.items():
    print ext, n_lines
