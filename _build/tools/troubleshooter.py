"""Publish the standalone Tower First Aid page at support/tower-first-aid.html.

Keeps the page as built, with three changes: embedded photos re-encoded smaller (WebP),
the logo links back to the Customer Support page in the current language, and ?lang=ja|en
in the URL picks the starting language.
"""
import base64
import io
import re
from pathlib import Path

from PIL import Image


def shrink(match):
    raw = base64.b64decode(match.group(2))
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    im.thumbnail((640, 640), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=62, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def must(s, old, new):
    if old not in s:
        raise SystemExit(f"troubleshooter: expected text not found: {old[:60]!r}")
    return s.replace(old, new, 1)


def build(src, out):
    s = Path(src).read_text(encoding="utf-8")
    s = re.sub(r"data:image/(jpeg|png);base64,([A-Za-z0-9+/=]+)", shrink, s)
    s = must(s, '<span class="brand">', '<a class="brand" id="brandlink" href="../support.html" '
                                         'title="Greentopia customer support" style="color:inherit;text-decoration:none">')
    s = must(s, '</span>\n    </span>\n    <span class="spacer">', '</span>\n    </a>\n    <span class="spacer">')
    s = must(s, 'try{ const s = localStorage.getItem("gt_lang"); if(s==="ja"||s==="en") lang = s; }catch(e){}',
             'try{ const q = new URLSearchParams(location.search).get("lang"); '
             'const s = (q==="ja"||q==="en") ? q : localStorage.getItem("gt_lang"); '
             'if(s==="ja"||s==="en") lang = s; }catch(e){}')
    s = must(s, 'document.documentElement.lang = (l==="ja" ? "ja" : "en");',
             'document.documentElement.lang = (l==="ja" ? "ja" : "en");\n  '
             'var bl = document.getElementById("brandlink"); '
             'if(bl) bl.href = (l==="ja" ? "../ja/support.html" : "../support.html");')
    # The source is an HTML fragment: give it a proper document start so browsers read it as UTF-8
    lead = '<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
    if 'name="viewport"' not in s:
        lead += '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    lead += '<link rel="icon" type="image/png" href="../G_only.png">\n'
    if "<html" not in s:
        s = lead + s
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s, encoding="utf-8")
    return out.stat().st_size
