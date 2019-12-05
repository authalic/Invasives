import os
import json
from os.path import join, getsize

"""
Merge a folder of JSON files into a single file containing all species
"""

collection = {
    "type": "FeatureCollection",
    "features": []
    }

folder = r"C:\projects\python\invasives\output_manual"

for (root,dirs,files) in os.walk(folder):
    outfile = join(root, "merged.json")

    for filename in files:

        filepath = join(root, filename)

        if getsize(filepath): # skip empty files

            with open(filepath, 'r') as f:
                filetext = f.read()
                spec = json.loads(filetext)
                collection["features"] += spec["features"]

    with open(outfile, 'w') as o:
        o.write(json.dumps(collection))
