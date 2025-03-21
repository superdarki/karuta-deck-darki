from PIL import Image
import numpy as np
import os, json, re, shutil, sys

path = os.environ.get('DECK_PATH', os.path.pardir)
if not os.path.isabs(path):
    path = os.path.join(os.path.dirname(__file__), path)

outpath = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.pardir, os.path.pardir, 'Deck Ancien Format')
if not os.path.isabs(outpath):
    outpath = os.path.join(os.path.dirname(__file__), outpath)

with open(os.path.join(path, 'deck.json'), "r") as file:
    meta = json.load(file)

images = [
    (
        m,
        np.array(Image.open(os.path.join(path, 'Visuals', m["image"])))
    ) for m in meta["cards"]
]

images_cut = [
    (
        m,
        re.sub(r"[\/\\\:\*\?\"\<\>\|]",""," ".join([meta['prefix'], m["anime"], m["numbering"], m["title"]])),
        Image.fromarray(im[35:1075,33:783])
    ) for (m,im) in images
]

for d in 'Sounds','Visuals':
    os.makedirs(os.path.join(outpath, d), exist_ok=True)
with open(os.path.join(outpath, meta["name"]+'.txt'), 'w') as file:
    for (m, n, im) in images_cut:
        print(n)
        file.write(n+"\n")
        im.save(os.path.join(outpath, 'Visuals', n+'.png'))
        shutil.copy(os.path.join(path, 'Sounds', m["audio"]), os.path.join(outpath, 'Sounds', n+'.mp3'))