"""Prepare the lab-sample photos for the app.

Reads the full-size phone photos in "Rock Samples", fixes their rotation, applies any crop
listed below, and writes web-sized copies to photos/ plus square thumbnails to photos/thumbs/.
Run it again whenever you add or change photos:

    python prepare_photos.py

To use a new photo, add a line to PHOTOS, then list it under that rock's `photos` in rock_data.py.
"""
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).parent
SRC = HERE / "Rock Samples"
OUT = HERE / "photos"
THUMBS = OUT / "thumbs"

FULL_SIZE = 1100    # longest side, pixels
THUMB_SIZE = 480    # square thumbnails for grids

# output name -> (file in "Rock Samples", optional crop as fractions of the upright photo:
#                 (left, top, right, bottom))
PHOTOS = {
    "granite-1": ("Granite.JPEG", None),
    "granite-2": ("Granite (2).JPEG", None),
    "diorite-1": ("Diorite.JPEG", None),
    "diorite-2": ("Diorite (2).JPEG", None),
    "gabbro-1": ("Gabbro.JPEG", None),
    "gabbro-2": ("Gabbro (2).JPEG", (0.19, 0.32, 0.87, 0.78)),   # small sample on a lot of white paper
    "basalt-1": ("Basalt.JPEG", None),
    "basalt-2": ("Basalt (with vesicles).JPEG", None),
    "obsidian-1": ("Obsidian (2).JPEG", None),
    "tuff-1": ("Tuff.JPEG", None),
    "tuff-2": ("Tuff (2).JPEG", None),                           # "Tuff (3).JPEG" is an exact duplicate
    "sandstone-1": ("Sandstone (2).JPEG", None),
    "sandstone-2": ("Sandstone.JPEG", None),
    "shale-1": ("Shale.JPEG", None),
    "shale-2": ("Shale (2).JPEG", None),
    "conglomerate-1": ("Conglomerate (2).JPEG", None),
    "conglomerate-2": ("Conglomerate.JPEG", None),               # drill core
    "slate-1": ("Slate.JPEG", None),
    "slate-2": ("Slate (2).JPEG", None),
    "schist-1": ("Schist.JPEG", None),
    "schist-2": ("IMG_4244.JPEG", None),                         # unlabeled file, confirmed schist
    "gneiss-1": ("Gneiss.JPEG", None),
    "gneiss-2": ("Gneiss (2).JPEG", (0.11, 0.0, 0.99, 0.9)),     # trims the table and blue paper
}


def main():
    OUT.mkdir(exist_ok=True)
    THUMBS.mkdir(exist_ok=True)
    for name, (filename, crop) in PHOTOS.items():
        im = ImageOps.exif_transpose(Image.open(SRC / filename)).convert("RGB")
        if crop:
            w, h = im.size
            l, t, r, b = crop
            im = im.crop((round(l * w), round(t * h), round(r * w), round(b * h)))
        thumb = ImageOps.fit(im, (THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
        im.thumbnail((FULL_SIZE, FULL_SIZE), Image.LANCZOS)
        im.save(OUT / f"{name}.jpg", quality=85, optimize=True, progressive=True)
        thumb.save(THUMBS / f"{name}.jpg", quality=82, optimize=True)
        print(f"{name}.jpg  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
