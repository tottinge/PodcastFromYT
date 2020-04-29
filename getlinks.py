import sys
import json
from box import Box

for filename in sys.argv[1:]:
    with open(filename) as source:
        info = Box(json.load(source))
        print(f'{info.webpage_url} | {info.title}')
