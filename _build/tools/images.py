"""Resize the chosen photos to web size (WebP) for the site.

Usage: python3 -I images.py PHOTOS_DIR OUT_DIR
"""
import sys
from pathlib import Path

import pillow_heif
from PIL import Image, ImageOps

pillow_heif.register_heif_opener()
SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
K = "claude keepers/"
M = "/mnt/user-data/uploads/BEST PHOTOS FOR MARKETING/"

# output name -> (source file, longest side in px)
HERO = 1400
CARD = 900
PHOTOS = {
    "home": (M + "Tower Farm/PXL_20251120_041116848.MP.jpg", HERO),
    "about": (M + "Founder/a.jpg", HERO),
    "contact": (K + "contact_hero.jpg", HERO),
    "education": (K + "education_hero.jpg", HERO),
    "integrated-curriculum": (K + "curriculum_hero.jpg", HERO),
    "events": (K + "events_hero.jpg", HERO),
    "home-towers": (K + "hometowers_hero2.jpg", HERO),
    "green-spaces": (M + "Lush Green Growth/S__9175065.jpg", HERO),
    "offices-coworking": (K + "offices_hero1.jpg", HERO),
    "partnerships": (K + "partnerships_hero1.jpg", HERO),
    "hotels": (K + "partnerships_hero2.jpg", HERO),
    "restaurants": (K + "partnerships_hero3.jpg", HERO),
    "residential-buildings": (K + "residential_hero1.jpg", HERO),
    "community-spaces": (K + "community_hero2.jpg", HERO),
    "sponsorship": (K + "sponsorship_hero1.jpg", HERO),
    "camps": (M + "Harvest/RZP Kids Harvest 2.jpg", HERO),
    "after-school-activities": ("afterschool_hero.jpg", HERO),
    "greentopia-labs": ("labs_hero.jpg", HERO),
    "workshops": (M + "Workshop/S__27443209_0.jpg", HERO),
    "grow": (M + "Harvest/PXL_20230807_085859509.jpg", HERO),
    "support": (M + "Harvest/PXL_20230424_012147938.jpg", HERO),
    "card-education": ("home_card_education.jpg", CARD),
    "card-green-spaces": ("home_card_greenspaces.jpg", CARD),
    "card-partnerships": ("home_card_partnerships.jpg", CARD),
    "card-workshop": ("home_highlight_workshop.jpg", CARD),
    "card-camps": (M + "Harvest/RZP Kids Harvest.jpg", CARD),
    "card-tower-lease": ("home_highlight_towerlease1.jpg", CARD),
}

OUT.mkdir(parents=True, exist_ok=True)
total = 0
for name, (src, size) in PHOTOS.items():
    im = ImageOps.exif_transpose(Image.open(SRC / src)).convert("RGB")
    im.thumbnail((size, size), Image.LANCZOS)
    dest = OUT / f"{name}.webp"
    im.save(dest, "WEBP", quality=76, method=6)
    total += dest.stat().st_size
    print(f"{name:26s} {im.size[0]}x{im.size[1]} {dest.stat().st_size // 1024} KB")

# Social share preview: 1200x630 crop of the lush rooftop towers
im = ImageOps.exif_transpose(Image.open(SRC / (M + "Lush Green Growth/S__9175065.jpg"))).convert("RGB")
ImageOps.fit(im, (1200, 630), Image.LANCZOS).save(OUT / "og.jpg", "JPEG", quality=82, optimize=True)
print(f"total {total // 1024} KB + og.jpg {(OUT / 'og.jpg').stat().st_size // 1024} KB")
