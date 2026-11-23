"""Japanese version of the site.

  python3 -I i18n.py extract SITE_DIR UNITS_JSON   -> every translatable English unit, with its pages
  python3 -I i18n.py build   SITE_DIR JA_TSV       -> writes SITE_DIR/ja/*.html from the English pages
  python3 -I i18n.py review  UNITS_JSON JA_TSV XLSX -> review spreadsheet for a native speaker

A "unit" is the inner HTML of a leaf block (p, h1-h4, li, blockquote, button, option, title),
a stray text node, or a text attribute (alt, placeholder, meta description). Units are keyed by
a short hash of their English, so the Japanese file survives page reordering.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Comment, Doctype

BLOCKS = ["title", "p", "h1", "h2", "h3", "h4", "li", "blockquote", "button", "option"]
ATTRS = ["alt", "placeholder"]
META = [("name", "description"), ("property", "og:title"), ("property", "og:description")]
ROOT_FILES = ("styles.css", "script.js", "G_only.png", "greentopia_wordmark.png", "images/", "logos/")
SITE = "https://greentopia.jp"
SKIP_PAGES = {"ja"}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def key(en):
    return hashlib.sha1(en.encode()).hexdigest()[:8]


def wanted(text):
    t = norm(text)
    if not re.search(r"[A-Za-z]", t):
        return False
    if re.fullmatch(r"[\w.+-]+@[\w.-]+|@\w+|https?://\S+|Instagram|Greentopia Japan|Greentopia", t):
        return False
    return True


def walk(soup, handle):
    """Call handle(en) -> replacement-or-None for every unit, applying replacements in place."""
    done = set()
    for el in soup.find_all(BLOCKS):
        if el.find(BLOCKS):
            continue
        inner = norm(el.decode_contents())
        if not wanted(BeautifulSoup(inner, "html.parser").get_text()):
            continue
        done.add(id(el))
        new = handle(inner)
        if new is not None:
            el.clear()
            for child in list(BeautifulSoup(new, "html.parser").contents):
                el.append(child)
    for node in list(soup.find_all(string=True)):
        if isinstance(node, (Comment, Doctype)) or node.parent.name in ("script", "style", "title"):
            continue
        if any(id(p) in done for p in node.parents):
            continue
        if not wanted(node):
            continue
        new = handle(norm(node))
        if new is not None:
            lead = " " if node[:1].isspace() else ""
            trail = " " if node[-1:].isspace() else ""
            node.replace_with(NavigableString(lead + new + trail))
    for attr in ATTRS:
        for el in soup.find_all(attrs={attr: True}):
            if wanted(el[attr]):
                new = handle(norm(el[attr]))
                if new is not None:
                    el[attr] = new
    for k, v in META:
        el = soup.find("meta", attrs={k: v})
        if el and wanted(el.get("content", "")):
            new = handle(norm(el["content"]))
            if new is not None:
                el["content"] = new


def pages(site):
    return sorted(p for p in Path(site).glob("*.html"))


def extract(site, out):
    units = {}
    for page in pages(site):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")

        def handle(en, page=page.name):
            u = units.setdefault(key(en), {"en": en, "pages": []})
            if page not in u["pages"]:
                u["pages"].append(page)
            return None
        walk(soup, handle)
    Path(out).write_text(json.dumps(units, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(units)} units, {sum(len(u['en']) for u in units.values())} chars")


def load_ja(tsv):
    table = {}
    for line in Path(tsv).read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            k, ja = re.split(r"\s*\|\|\|\s*|\t", line, maxsplit=1)
            table[k.strip()] = ja.strip()
    return table


def relink(soup, page_name):
    for el in soup.find_all(href=True) + soup.find_all(src=True):
        attr = "href" if el.has_attr("href") else "src"
        v = el[attr]
        if v.startswith(ROOT_FILES):
            el[attr] = "../" + v
        elif v.startswith("/") and v.endswith(".html"):
            el[attr] = "/ja" + v
    form = soup.find("form", attrs={"action": True})
    if form and form["action"].startswith("/") and not form["action"].startswith("/ja/"):
        form["action"] = "/ja" + form["action"]


def add_switch(soup, page_name, lang):
    """Language switcher + hreflang links. lang is the language of this soup."""
    path = "" if page_name == "index.html" else page_name
    head = soup.find("head")
    for hl, href in (("en", f"{SITE}/{path}"), ("ja", f"{SITE}/ja/{path}")):
        head.append(soup.new_tag("link", rel="alternate", hreflang=hl, href=href))
    tools = soup.find("div", class_="header-tools")
    rooted = page_name in ("404.html", "thanks.html")
    if lang == "en":
        target = f"/ja/{page_name}" if rooted else f"ja/{page_name}"
        a = soup.new_tag("a", attrs={"class": "lang-toggle", "href": target, "lang": "ja", "hreflang": "ja"})
        a.string = "日本語"
    else:
        target = f"/{page_name}" if rooted else f"../{page_name}"
        a = soup.new_tag("a", attrs={"class": "lang-toggle", "href": target, "lang": "en", "hreflang": "en"})
        a.string = "English"
    tools.insert(0, a)


def build(site, tsv):
    site = Path(site)
    table = load_ja(tsv)
    out = site / "ja"
    out.mkdir(exist_ok=True)
    missing = {}
    for page in pages(site):
        src = page.read_text(encoding="utf-8")
        ja = BeautifulSoup(src, "html.parser")

        def handle(en, page=page.name):
            k = key(en)
            if k in table:
                return table[k]
            missing.setdefault(k, en)
            return None
        walk(ja, handle)
        ja.find("html")["lang"] = "ja"
        relink(ja, page.name)
        add_switch(ja, page.name, "ja")
        (out / page.name).write_text(str(ja), encoding="utf-8")
        en = BeautifulSoup(src, "html.parser")
        add_switch(en, page.name, "en")
        page.write_text(str(en), encoding="utf-8")
    print(f"built {len(pages(site))} Japanese pages; {len(missing)} untranslated units")
    for k, en in list(missing.items())[:40]:
        print(f"  missing {k}: {en[:90]}")
    return missing


def review(units_json, tsv, xlsx):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    units = json.loads(Path(units_json).read_text(encoding="utf-8"))
    table = load_ja(tsv)
    order = ["index", "education", "after-school-activities", "greentopia-labs", "integrated-curriculum",
             "camps", "workshops", "green-spaces", "home-towers", "residential-buildings",
             "offices-coworking", "community-spaces", "partnerships", "restaurants", "hotels",
             "sponsorship", "events", "about", "contact", "thanks", "404"]
    names = {"index": "Home", "404": "Page not found"}
    wb = Workbook()
    ws = wb.active
    ws.title = "Translation review"
    ws.append(["ID", "Page", "English", "Japanese (current)", "Revision (leave blank if OK)", "Notes"])
    seen = set()
    shared = [k for k, u in units.items() if len(u["pages"]) > 3]
    rows = [(k, "All pages (header, footer, menus)") for k in shared]
    seen.update(shared)
    for p in order:
        for k, u in units.items():
            if k not in seen and p + ".html" in u["pages"]:
                rows.append((k, names.get(p, p.replace("-", " ").title())))
                seen.add(k)
    for k, page in rows:
        en = BeautifulSoup(units[k]["en"], "html.parser").get_text()
        ja = BeautifulSoup(table.get(k, ""), "html.parser").get_text()
        ws.append([k, page, en, ja, "", ""])
    for col, w in zip("ABCDEF", (10, 22, 60, 60, 45, 30)):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1D263B")
    for r in range(2, ws.max_row + 1):
        ws.cell(r, 5).fill = PatternFill("solid", fgColor="F4F7EC")
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions
    for row in ws.iter_rows():
        for c in row:
            c.font = Font(name="Arial", bold=c.row == 1, color="FFFFFF" if c.row == 1 else "000000")
    guide = wb.create_sheet("How to use", 0)
    lines = [
        ("Greentopia website — Japanese translation review", True),
        ("", False),
        ("1. Open the “Translation review” tab. Each row is one piece of text on the website.", False),
        ("2. Read the English (column C) and the current Japanese (column D).", False),
        ("3. If the Japanese is fine, leave column E (green) blank.", False),
        ("4. If it should change, type the full corrected Japanese in column E. Use column F for any comment.", False),
        ("5. Do not edit columns A–D. The ID in column A tells Claude exactly which text to update.", False),
        ("6. Rows marked “All pages” are the menu, buttons and footer that appear on every page.", False),
        ("", False),
        ("Example of a revision:", True),
        ("Column D (current): 私たちについて", False),
        ("Column E (revision): Greentopiaについて", False),
        ("Column F (notes): Sounds more natural for the menu", False),
        ("", False),
        ("Names: Japanese pages show people’s names in English letters. If you want a name in kanji or katakana "
         "(e.g. Emiko Hirayama), write it in column E.", False),
        ("Live Japanese site: https://greentopia-japan.netlify.app/ja/", False),
    ]
    for i, (text, bold) in enumerate(lines, 1):
        c = guide.cell(i, 1, text)
        c.font = Font(name="Arial", bold=bold, size=14 if i == 1 else 11)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    guide.column_dimensions["A"].width = 110
    wb.active = 0
    wb.save(xlsx)
    print(f"review rows: {len(rows)}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"extract": extract, "build": build, "review": review}[cmd](*sys.argv[2:])
