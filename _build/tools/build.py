"""Turn the v13 prototype into the production site.

Usage: python3 -I build.py SRC_DIR OUT_DIR
Re-runnable: always rebuilds OUT_DIR's site files from SRC_DIR.
"""
import html
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages_extra as X  # noqa: E402
import troubleshooter  # noqa: E402

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
SKIP = {"README.md", "TEST_REPORT.json", "event-detail-sample.html", "desktop.ini"}  # from the v13 source
IG = "https://www.instagram.com/greentopiajapan/"
WINTER_FORM = ("https://docs.google.com/forms/d/e/1FAIpQLSe8XU4l0FUitqK0MfBZEdrmbVgBIxb_nnEMkcwAuDDk9ew6kA/"
               "viewform")


def must_replace(s, old, new, fname, count=1):
    if old not in s:
        raise SystemExit(f"[{fname}] expected text not found: {old[:70]!r}")
    return s.replace(old, new, count)


def common(s, fname):
    # Strip stray control characters left by earlier editing tools
    s = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", s)
    # Titles
    s = s.replace(" | Greentopia Japan Prototype</title>", " | Greentopia Japan</title>")
    # Head extras: description, favicon, social preview
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    m = re.search(r'<div class="hero-copy">.*?<p>(.*?)</p>', s, re.S)
    desc = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else \
        "Hydroponic urban farming education and installations in Tokyo."
    desc = html.escape(html.unescape(desc), quote=True)
    head = (f'<meta name="description" content="{desc}">'
            f'<link rel="icon" type="image/png" href="G_only.png">'
            f'<meta property="og:type" content="website">'
            f'<meta property="og:site_name" content="Greentopia Japan">'
            f'<meta property="og:title" content="{html.escape(title, quote=True)}">'
            f'<meta property="og:description" content="{desc}">')
    s, n = re.subn(r'<link (?:rel="stylesheet" href="styles.css"|href="styles.css" rel="stylesheet")/?>',
                   lambda m: head + m.group(0), s, count=1)
    if not n:
        raise SystemExit(f"[{fname}] stylesheet link not found")
    # Language toggle hidden until a Japanese version exists
    s, n = re.subn(r'<button class="lang-toggle"[^>]*>.*?</button>', "", s, count=1)
    if not n:
        raise SystemExit(f"[{fname}] language toggle not found")
    # Social links: Instagram only until Facebook/LinkedIn URLs exist
    s = re.sub(r'<div class="mobile-social">[^<]*</div>',
               f'<div class="mobile-social"><a href="{IG}" target="_blank" rel="noopener">Instagram</a></div>', s)
    s = re.sub(r'<a href="#(?:facebook|linkedin)"[^>]*>[^<]*</a>', "", s)
    # Unfinished order links go to the contact form with the topic preselected
    s = s.replace('href="#tower-order-form-placeholder"', 'href="contact.html?interest=tower"')
    s = s.replace("<p>FORM PLACEHOLDER: Replace this link with the live tower order form URL.</p>",
                  "<p>Tell us your space and we’ll recommend the right tower.</p>")
    s = s.replace("<p>FORM PLACEHOLDER: Replace with live tower-order form URL.</p>",
                  "<p>Tell us your space and we’ll recommend the right tower.</p>")
    s = s.replace('<div class="footer-links"><a href="mailto:info@greentopia.jp">',
                  '<div class="footer-links"><a href="support.html">Customer support</a>'
                  '<a href="mailto:info@greentopia.jp">')
    s = s.replace('<a href="contact.html">Contact</a><div class="mobile-social">',
                  '<a href="contact.html">Contact</a><a href="support.html">Customer support</a>'
                  '<div class="mobile-social">')
    for old, new in PRICE_FIXES:
        s = s.replace(old, new)
    if "¥10,000" in s:
        raise SystemExit(f"[{fname}] old ¥10,000 price still present")
    return s


PLANS = ("Leases start with a 3-month trial at ¥13,000/month. After that, choose the plan that fits: "
         "¥11,000/month if you care for the tower yourself, ¥15,000/month with a monthly service visit, "
         "or ¥18,000/month with a weekly service visit.")
PRICE_FIXES = [
    ("Tower leases start from ¥10,000/month with a 3-month minimum.",
     "Tower leases start from ¥11,000/month after a 3-month trial at ¥13,000/month."),
    ("Leases start from ¥10,000/month, depending on tower type, location, and setup.",
     "Leases start from ¥11,000/month, depending on the service level you choose."),
    ("Tower leases start from ¥10,000/month, depending on tower type, location, and setup, with a 3-month minimum.",
     PLANS),
    ("Tower leases start from ¥10,000/month, depending on tower type, location, and setup. We offer two sizes",
     PLANS + " We offer two sizes"),
    (" The minimum lease is 3 months.", ""),
    ("Tower leases from ¥10,000/month, depending on tower type, location, and setup.",
     "Tower leases from ¥11,000/month, depending on the service level you choose."),
    ("Maintenance contract: available separately for growers who want regular professional check-ins.",
     "Service visits: included in the monthly and weekly plans for growers who want regular professional "
     "check-ins."),
    ("For those who prefer hands-off growing, we offer a separate maintenance contract with regular visits — "
     "frequency ranges from weekly to monthly depending on your needs.",
     "For hands-off growing, choose a plan with monthly or weekly service visits."),
]

PAGE_FIXES = {
    "index.html": [
        ("<p>Next workshop: [DATE TBD]. Hands-on hydroponics for families and curious growers. "
         "No experience needed — just show up and get your hands wet.</p>",
         "<p>Saturday, December 12, 1:00–3:00 PM at Art Farm Ikejiri. Hands-on hydroponics for families and "
         "curious growers. No experience needed — just show up and get your hands wet.</p>"),
        ("<p>Summer 2026: Week-long STEM day camps for ages 6–14. Hydroponics, experiments, field trips, "
         "and fresh harvests every day. Spaces are limited.</p>",
         "<p>December 14–23: pick any days. Hydroponics, science, engineering, and creative making for ages 5 "
         "and up. Registration is open now.</p>"),
        ("<h3>Summer Camp</h3>", "<h3>Winter Discovery Camp</h3>"),
        (re.compile(r'<div class="instagram-placeholder">.*?</p></div>', re.S),
         f'<div class="instagram-cta"><p>Harvests, workshops, and behind-the-scenes moments from our '
         f'classrooms and towers.</p><a class="button primary" href="{IG}" target="_blank" '
         f'rel="noopener">Follow @greentopiajapan</a></div>'),
        ("<h2>Instagram preview</h2>", "<h2>Follow along on Instagram</h2>"),
    ],
    "contact.html": [
        ('<form class="prototype-form" onsubmit="event.preventDefault();alert(\'Prototype only: connect '
         'this form to Wix Forms, STORES, or another service.\');">',
         '<form class="prototype-form" name="contact" method="POST" action="/thanks.html" '
         'data-netlify="true" netlify-honeypot="bot-field" enctype="multipart/form-data">'
         '<input type="hidden" name="form-name" value="contact">'
         '<p hidden><label>Leave this empty<input name="bot-field"></label></p>'),
        ('<label>Name<input placeholder', '<label>Name<input name="name" placeholder'),
        ('<label>Email<input placeholder', '<label>Email<input name="email" placeholder'),
        ('<label>Organization<input placeholder', '<label>Organization<input name="organization" placeholder'),
        ('<label>Area / location<input placeholder', '<label>Area / location<input name="area" placeholder'),
        ('<select id="interest-select">', '<select id="interest-select" name="interest">'),
        ('<option value="workshops">Workshop</option>',
         '<option value="workshops">Workshop</option><option value="camps">Camps</option>'),
        ('<option value="tower">Tower lease or purchase</option>',
         '<option value="tower">Tower lease</option><option value="customer-support">Existing customer: visit, '
         'cleaning, or supplies</option>'),
        ('<input type="file"/>', '<input type="file" name="attachment"/>'),
        ('<textarea placeholder', '<textarea name="message" required placeholder'),
        ('<button class="button cta-orange">', '<button type="submit" class="button cta-orange">'),
        ('href="#summer-camp-registration-placeholder"', f'href="{WINTER_FORM}" target="_blank" rel="noopener"'),
        ("<h3>Summer Camp Registration Form</h3><p>FORM PLACEHOLDER: Replace with the live summer camp "
         "registration URL.</p>",
         "<h3>Winter Camp Registration</h3><p>Winter Discovery Camp, December 14–23. Pick your days and "
         "register.</p>"),
        ("<p>GOOGLE FORM PLACEHOLDER: Replace with the live seedling order form URL.</p>",
         "<p>Order seedlings through our Google Form.</p>"),
        ('<h3>Order Seedlings Form</h3><p>Order seedlings through our Google Form.</p></a>',
         '<h3>Order Seedlings Form</h3><p>Order seedlings through our Google Form.</p></a>'
         '<a class="feature-card" href="support.html"><h3>Customer Support</h3><p>Already growing with us? '
         'Troubleshooting, seedlings, and visit requests.</p></a>'),
    ],
    "events.html": [
        ("<p>May 2026: Family Workshop at Ryozan Park — 12 families, tower planting, and salad tasting. March 2026: "
         "Green STEM Club harvest celebration at Seisen International School. January 2026: Hydroponics intro "
         "workshop for BST parents. More photos",
         "<p>Highlights from previous programs coming soon! More photos"),
        (re.compile(r'<a class="event-row" href="event-detail-sample.html">.*?</a>\s*'
                    r'<a class="event-row" href="summer-camps.html">.*?</a>', re.S),
         '<a class="event-row" href="workshops.html"><div class="event-date"><strong>Dec 12</strong>'
         '<span>Saturday</span></div><div class="event-summary"><span class="event-type">Workshop</span>'
         '<h3>Family Hydroponics Workshop</h3><p>1:00–3:00 PM · Art Farm Ikejiri · Hands-on tower planting '
         'for families. All ages welcome.</p></div><span class="event-arrow">→</span></a>\n'
         '    <a class="event-row" href="summer-camps.html"><div class="event-date"><strong>Dec 14–23'
         '</strong><span>Pick any days</span></div><div class="event-summary"><span class="event-type">Camp'
         '</span><h3>Winter Discovery Camp 2026</h3><p>9:00–17:30 · J\'s International School, Motoazabu · '
         'Mornings, afternoons, or full days, ages 5 and up. Registration open.</p></div>'
         '<span class="event-arrow">→</span></a>'),
    ],
    "about.html": [
        ("We deliver, set up, and walk you through everything. At the end of your lease you can purchase, renew, "
         "or return the tower.",
         "We deliver, set up, and walk you through everything. At the end of your lease you can renew or return "
         "the tower."),
        ("Seedlings are ¥200–300 per plant, depending on variety. Order as many or as few as you need, anytime.",
         "Seedlings are ¥200–300 per rockwool cube (one planting port), depending on variety. Each cube usually "
         "holds 2–4 plants. Order as many or as few as you need, anytime."),
        ("easiest starting point.</p>",
         'easiest starting point. <a href="grow.html">See the full list of varieties</a>.</p>'),
    ],
    "green-spaces.html": [
        ("Leases start with a 3-month trial at ¥13,000/month. After that, choose the plan that fits: ¥11,000/month "
         "if you care for the tower yourself, ¥15,000/month with a monthly service visit, or ¥18,000/month with a "
         "weekly service visit. We deliver, set up, and walk you through everything. At the end of your lease, you "
         "can renew, purchase the tower, or we pick it up and reset. No long-term commitment required.",
         'Home tower leases start with a 3-month trial at ¥13,000/month, then from ¥11,000/month depending on how '
         'much care you want from us. We deliver, set up, and walk you through everything. '
         '<a href="home-towers.html#plans">See the lease plans</a>. For buildings, offices, and community spaces, we '
         'quote each project after a free site assessment.'),
        ("<h2>Starter kits and maintenance</h2>", "<h2>Seedlings and supplies</h2>"),
        ("New growers can add a Starter Kit, approximately ¥4,000–5,000, that includes nutrients, pH buffers, and an "
         "initial set of seedlings. Seedlings can be reordered anytime from our online form at ¥200–300 per plant. "
         "For hands-off growing, choose a plan with monthly or weekly service visits.",
         "Trial customers get a free starter set. If you already have a tower or grow hydroponically at home, we "
         "can also supply starter sets, nutrients, and seedlings. Seedlings are ¥200–300 per rockwool cube, and each "
         'cube usually holds 2–4 plants. Order seedlings through our online form, or <a href="support.html">contact '
         "us</a> for other supplies. For hands-off growing, choose a plan with monthly or weekly service visits."),
        ('<h3>Community Spaces</h3><p>Share farms, workshops, and neighborhood engagement.</p></a>',
         '<h3>Community Spaces</h3><p>Share farms, workshops, and neighborhood engagement.</p></a>'
         '<a class="feature-card" href="grow.html"><h3>What You Can Grow</h3>'
         '<p>Varieties for indoor and outdoor towers.</p></a>'),
    ],
    "education.html": [
        ("<h3>Summer Camps</h3><p>Seasonal and vacation programs.</p>",
         "<h3>Camps</h3><p>Winter, spring, summer, and fall camps.</p>"),
    ],
    "workshops.html": [
        ('<p>Check our <a href="events.html">Events page</a> for the latest workshop schedule, or contact us '
         'to arrange a private workshop for your group.</p>',
         '<p><strong>Family Hydroponics Workshop</strong> · Saturday, December 12, 1:00–3:00 PM · Art Farm '
         'Ikejiri. <a href="contact.html?interest=workshops">Ask us to save you a spot</a>.</p>'
         '<p>Want a private workshop for your school, company, or community group? Contact us to arrange one. '
         'New dates are also posted on our <a href="events.html">Events page</a> and Instagram.</p>'),
    ],
    "after-school-activities.html": [
        (re.compile(r'<section class="content-section"><span class="eyebrow">In action</span>.*?</section>',
                    re.S), ""),
    ],
    "community-spaces.html": [
        (" CASE STUDY PLACEHOLDER: Add the Art Farm Ikejiri or Ryozan Park rooftop story when ready.", ""),
    ],
    "partnerships.html": [
        (" CASE STUDY PLACEHOLDER: Add real project examples and outcomes when ready.", ""),
    ],
}

EXTRA_CSS = """
/* production overrides */
.text-placeholder{padding:0;border:0;background:none}.text-placeholder p{margin:10px 0 0;color:var(--muted)}
.instagram-cta{text-align:center}.instagram-cta p{color:var(--muted);margin:0 0 16px}
.simple-page{text-align:center;padding:60px 24px}.simple-page p{color:var(--muted);margin:12px 0 24px}
.mobile-social a{color:var(--green);font-weight:700}
a.lang-toggle{display:inline-flex;align-items:center;font-size:14px;font-weight:700;white-space:nowrap}
html[lang=ja] body{font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN","Yu Gothic UI","Yu Gothic",Meiryo,"Noto Sans JP",Arial,sans-serif;line-height:1.75;line-break:strict}
html[lang=ja] h1{font-size:clamp(32px,4.2vw,54px);line-height:1.25;word-break:auto-phrase}
html[lang=ja] h2,html[lang=ja] h3{line-height:1.4;word-break:auto-phrase}
html[lang=ja] .eyebrow{letter-spacing:.08em}
@media(max-width:900px){html[lang=ja] h1{font-size:30px}}
.hero-photo{display:block;width:100%;height:420px;object-fit:cover;border-radius:22px}.hero-premium .hero-photo{height:490px;object-position:50% 20%}
.photo-card{padding:0;overflow:hidden}.photo-card h3,.photo-card p{padding:0 18px}.photo-card p{padding-bottom:18px}
.card-photo{display:block;width:100%;height:180px;object-fit:cover}
@media(max-width:900px){.hero-photo,.hero-premium .hero-photo{height:260px}}
.logo-strip{display:flex;flex-wrap:wrap;justify-content:center}.logo-strip div{flex:0 0 calc(20% - 12px)}
@media(max-width:900px){.logo-strip div{flex-basis:calc(33.33% - 7px)}}
"""


def apply_fixes(s, fname):
    for old, new in PAGE_FIXES.get(fname, []):
        if isinstance(old, re.Pattern):
            s, n = old.subn(new, s, count=1)
            if not n:
                raise SystemExit(f"[{fname}] pattern not found: {old.pattern[:70]!r}")
        else:
            s = must_replace(s, old, new, fname)
    return s


def simple_page(template, title, heading, body, button_href, button_text):
    head, rest = template.split("<main", 1)
    tail = rest.split("</main>", 1)[1]
    head = re.sub(r"<title>.*?</title>", f"<title>{title} | Greentopia Japan</title>", head)
    head = re.sub(r'(<meta (?:name="description"|property="og:(?:title|description)") content=")[^"]*"',
                  lambda m: m.group(1) + html.escape(heading, quote=True) + '"', head)
    main = (f'<main class="site-main"><section class="content-section simple-page"><h1>{heading}</h1>'
            f'<p>{body}</p><a class="button primary" href="{button_href}">{button_text}</a></section></main>')
    page = head + main + tail
    # Root-relative links so the page works at any URL depth (needed for 404s on old nested paths)
    return re.sub(r'(href|src)="(?!https?:|mailto:|/|#)([^"]+)"', r'\1="/\2"', page)


IMAGES = Path(__file__).resolve().parent.parent / "src" / "images"
HERO_ALT = {
    "index": "Sunlit Greentopia hydroponic towers full of greens on a Tokyo rooftop",
    "about": "Founder Richard Mayus tending a hydroponic tower on a Tokyo rooftop",
    "contact": "Hand holding a freshly harvested hydroponic lettuce with roots",
    "education": "Students gathered around a hydroponic tower on a school terrace",
    "integrated-curriculum": "Greentopia educator leading a class lesson",
    "events": "Families at a Greentopia rooftop workshop",
    "home-towers": "Hydroponic towers on a Tokyo balcony",
    "green-spaces": "Lush hydroponic towers on a rooftop terrace",
    "offices-coworking": "Hydroponic tower in an office space",
    "partnerships": "Hydroponic planters built into a restaurant interior",
    "hotels": "Greens growing in an upscale hospitality interior",
    "restaurants": "Hydroponic planter boxes with fresh greens",
    "residential-buildings": "Row of hydroponic towers on a Tokyo rooftop",
    "community-spaces": "Hydroponic towers in a shared rooftop greenhouse",
    "sponsorship": "Children holding bowls of freshly harvested greens",
    "summer-camps": "Summer camp field trip to a Tokyo garden",
    "after-school-activities": "After-school students working with a Greentopia instructor",
    "greentopia-labs": "Greentopia Labs students running a science experiment",
    "workshops": "Families sharing a meal at a rooftop hydroponics workshop",
}
CARD_PHOTOS = {  # homepage card link -> (image, alt)
    "education.html": ("card-education", "Students at a Greentopia class"),
    "green-spaces.html": ("card-green-spaces", "Towers growing on a terrace"),
    "partnerships.html": ("card-partnerships", "Rooftop tower installation"),
    "events.html": ("card-workshop", "Rooftop workshop group"),
    "summer-camps.html": ("card-camps", "Young campers carrying freshly harvested greens"),
    "home-towers.html": ("card-tower-lease", "Home tower in a living room"),
}
HERO_RE = re.compile(r'<div class="image-placeholder hero-image">.*?</span>\s*</div>', re.S)


def add_photos(s, fname):
    page = fname[:-5]
    key = "home" if page == "index" else page
    if page in HERO_ALT:
        img = (f'<img class="hero-image hero-photo" src="images/{key}.webp" alt="{HERO_ALT[page]}"'
               f'{"" if page == "index" else " loading=\"lazy\""}>')
        s, n = HERO_RE.subn(img, s, count=1)
        if not n:
            raise SystemExit(f"[{fname}] hero placeholder not found")
    if page == "index":
        for href, (img, alt) in CARD_PHOTOS.items():
            s = must_replace(s, f'<a class="feature-card" href="{href}">',
                             f'<a class="feature-card photo-card" href="{href}"><img class="card-photo" '
                             f'src="images/{img}.webp" alt="{alt}" loading="lazy">', fname)
    # Social share image (absolute URL so it works once greentopia.jp points here)
    s = s.replace('<meta property="og:type" content="website">',
                  '<meta property="og:type" content="website">'
                  '<meta property="og:image" content="https://www.greentopia.jp/images/og.jpg">')
    return s


CTA_INTEREST = {  # page -> contact-form topic for the hero button
    "about": "", "after-school-activities": "after-school-activities", "community-spaces": "site-assessment",
    "education": "school-program", "green-spaces": "tower", "greentopia-labs": "greentopia-labs",
    "hotels": "partnership", "integrated-curriculum": "school-program",
    "offices-coworking": "site-assessment", "partnerships": "site-assessment",
    "residential-buildings": "site-assessment", "restaurants": "partnership", "sponsorship": "sponsorship",
    "workshops": "workshops",
}

CAMPS_MAIN = f'''<main class="site-main"><section class="hero"><div class="hero-copy"><span class="eyebrow">Camps</span>
<h1>Hands-on STEM camps every school break.</h1>
<p>Winter, spring, summer, and fall camps with hydroponics, science, engineering, and outdoor discovery. Ages 5 and up, in Motoazabu, Tokyo.</p>
<div class="hero-actions"><a class="button cta-orange" href="{WINTER_FORM}" target="_blank" rel="noopener">Register for Winter Camp</a></div></div>
<img class="hero-image hero-photo" src="images/camps.webp" alt="Young campers harvesting greens from rooftop hydroponic towers"></section>

<section class="content-section camp-feature"><span class="eyebrow">Now enrolling</span><h2>Winter Discovery Camp 2026</h2>
<p class="section-intro"><strong>December 14–23, 2026</strong>, 10 days including the weekend. Pick any days and mix mornings, afternoons, and full days, from a single session to all ten days.</p>
<div class="card-grid session-grid">
<div class="feature-card session-card"><span class="event-type">Morning · Daytime Discovery</span><h3>9:00–14:00 <span class="price">¥10,000 / day</span></h3><p>Build, grow, and investigate: science and technology, engineering projects, hydroponics, urban farming, and outdoor discovery, with a lunch break.</p></div>
<div class="feature-card session-card"><span class="event-type">Afternoon · Creative Explorations</span><h3>14:00–17:30 <span class="price">¥7,500 / day</span></h3><p>Nature-inspired art, eco-crafts, sustainability challenges, and relaxed creative making.</p></div>
<div class="feature-card session-card"><span class="event-type">Full day · Both experiences</span><h3>9:00–17:30 <span class="price">¥15,000 / day</span></h3><p>Morning and afternoon together. Save ¥2,500 compared with booking the sessions separately.</p></div>
</div>
<div class="event-detail-grid camp-details">
<div><strong>Ages</strong><p>5 and up</p></div>
<div><strong>Location</strong><p>The Greentopia School, 3rd floor, J's International School, 2-12-14 Motoazabu, Minato-ku, Tokyo</p></div>
<div><strong>Booking</strong><p>Any combination of days and sessions. No minimum number of days.</p></div>
</div>
<div class="inline-actions"><a class="button cta-orange" href="{WINTER_FORM}" target="_blank" rel="noopener">Pick your days and register</a></div>
<p class="fine-print">Registering requests a place. We'll confirm your booking and email the total and payment instructions. Spaces are limited, and camps run subject to minimum enrollment. Questions? <a href="mailto:info@greentopia.jp">info@greentopia.jp</a></p>
</section>

<section class="content-section"><span class="eyebrow">All year round</span><h2>Upcoming camps</h2>
<p class="section-intro">We run a camp every school break, all year round.</p>
<div class="card-grid">
<a class="feature-card" href="contact.html?interest=camps"><span class="event-type">Spring 2027</span><h3>Spring Camp</h3><p>During the spring break. Dates coming soon. Contact us to hear first.</p></a>
<a class="feature-card" href="contact.html?interest=camps"><span class="event-type">Summer 2027</span><h3>Summer Camp</h3><p>Our longest camp, across the summer break. Registration opens in spring.</p></a>
<a class="feature-card" href="contact.html?interest=camps"><span class="event-type">Fall 2027</span><h3>Fall Camp</h3><p>During the autumn school break. Dates to be announced.</p></a>
</div></section>

<section class="content-section"><span class="eyebrow">The experience</span><h2>What campers do</h2>
<div class="text-placeholder"><p>Every Greentopia camp blends hydroponics, science experiments, engineering projects, outdoor exploration, and creative making. Mornings focus on bigger STEM and growing projects; afternoons are for art, crafts, and hands-on sustainability challenges. Themes change each season, so returning campers always have something new. Past themes include “Seed to Smoothie,” “Farm Engineers,” “Bug Detectives,” and “Future Farmers.”</p>
<p>Outdoor activities and field trips to local parks and gardens are part of most camps, weather permitting.</p></div></section>
</main>'''

CAMPS_CSS = """
.session-card .event-type{display:block}.session-card h3{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px}
.price{color:var(--orange)}.camp-details{margin-top:15px}.camp-details strong{color:var(--forest)}
.fine-print{margin-top:14px;font-size:13px;color:var(--muted)}.fine-print a{color:var(--green);font-weight:700}
.feature-card .event-type{display:block}
"""


def camps_page(summer_src):
    s = common(summer_src, "summer-camps.html")
    head, rest = s.split("<main", 1)
    tail = rest.split("</main>", 1)[1]
    head = head.replace("<title>Summer Camps | Greentopia Japan</title>", "<title>Camps | Greentopia Japan</title>")
    desc = ("Winter, spring, summer, and fall STEM camps in Tokyo with hydroponics, science, and outdoor "
            "discovery. Ages 5 and up. Winter Discovery Camp: December 14–23, 2026.")
    head = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*"',
                  lambda m: m.group(1) + html.escape(desc, quote=True) + '"', head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*"', r'\1Camps | Greentopia Japan"', head)
    page = head + CAMPS_MAIN + tail
    return add_photos(page, "camps.html")


def hero_img(key, alt):
    return f'<img class="hero-image hero-photo" src="images/{key}.webp" alt="{alt}" loading="lazy">'


def new_page(template, title, desc, main):
    head, rest = template.split("<main", 1)
    tail = rest.split("</main>", 1)[1]
    head = re.sub(r"<title>.*?</title>", f"<title>{title} | Greentopia Japan</title>", head)
    head = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*"',
                  lambda m: m.group(1) + html.escape(desc, quote=True) + '"', head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*"',
                  lambda m: m.group(1) + html.escape(title, quote=True) + ' | Greentopia Japan"', head)
    return head + main + tail


def site_wide(s, fname):
    """Changes that apply to every page after the per-page fixes."""
    s = s.replace('href="summer-camps.html"', 'href="camps.html"')
    s = s.replace("Workshop and summer camp pricing varies", "Workshop and camp pricing varies")
    s = s.replace("summer camps, and workshops", "seasonal camps, and workshops")
    page = fname[:-5]
    if page in CTA_INTEREST:
        topic = CTA_INTEREST[page]
        target = f"contact.html?interest={topic}" if topic else "contact.html"
        s = must_replace(s, '<a class="button cta-orange">', f'<a class="button cta-orange" href="{target}">', fname)
    return s


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pages = {}
    for p in sorted(SRC.rglob("*")):
        rel = p.relative_to(SRC)
        if p.is_dir() or rel.name in SKIP:
            continue
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix == ".html":
            s = p.read_text(encoding="utf-8")
            if rel.name == "summer-camps.html":
                camps = camps_page(s)
                (OUT / "camps.html").write_text(site_wide(camps, "camps.html"), encoding="utf-8")
                continue
            s = site_wide(add_photos(apply_fixes(common(s, rel.name), rel.name), rel.name), rel.name)
            if "PLACEHOLDER" in s.replace("image-placeholder", "").replace("HERO IMAGE PLACEHOLDER", ""):
                print(f"warning: leftover placeholder text in {rel}")
            if rel.name == "home-towers.html":
                main = X.HOME_TOWERS_MAIN.replace("HERO_PLACEHOLDER", hero_img("home-towers", HERO_ALT["home-towers"]))
                s = re.sub(r"<main.*?</main>", lambda m: main, s, count=1, flags=re.S)
            pages[rel.name] = s
            dest.write_text(s, encoding="utf-8")
        elif p.name == "styles.css":
            dest.write_text(p.read_text(encoding="utf-8") + EXTRA_CSS + CAMPS_CSS + X.EXTRA_CSS, encoding="utf-8")
        else:
            shutil.copy2(p, dest)
    if IMAGES.exists():  # fresh photo exports replace the published set; otherwise keep what's there
        if (OUT / "images").exists():
            shutil.rmtree(OUT / "images")
        shutil.copytree(IMAGES, OUT / "images")
    (OUT / "_redirects").write_text(
        "# Old Wix pages (www.greentopia.jp) -> new pages\n"
        "/home-1  /  301\n/home-1-1  /  301\n/about-us  /about.html  301\n/business  /partnerships.html  301\n"
        "/project-spotlight-1  /education.html  301\n/project-spotlight-1-1  /education.html  301\n"
        "# Old Wix language subdomains (once added as domain aliases in Netlify)\n"
        "https://ja.greentopia.jp/*  https://www.greentopia.jp/ja/  301!\n"
        "https://en.greentopia.jp/*  https://www.greentopia.jp/  301!\n"
        "# Renamed pages\n"
        "/summer-camps.html  /camps.html  301\n/summer-camps  /camps  301\n"
        "/ja/summer-camps.html  /ja/camps.html  301\n"
        "# Private build files and Japanese 404\n"
        "/_build/*  /404.html  404!\n/ja/*  /ja/404.html  404\n",
        encoding="utf-8")
    tpl = pages["about.html"]
    (OUT / "grow.html").write_text(new_page(
        tpl, "What You Can Grow",
        "Leafy greens, herbs, fruiting vegetables, and flowers you can grow in a Greentopia hydroponic tower, "
        "indoors or outdoors, plus this season's picks.",
        X.grow_main().replace("HERO_PLACEHOLDER", hero_img(
            "grow", "Freshly harvested kale, chard, herbs, cucumbers, and tomatoes from a tower"))), encoding="utf-8")
    (OUT / "support.html").write_text(new_page(
        tpl, "Customer Support",
        "Help for Greentopia growers: tower troubleshooting, seedling orders, maintenance visits, and supplies.",
        X.SUPPORT_MAIN.replace("HERO_PLACEHOLDER", hero_img(
            "support", "Harvesting fresh bok choy from a Greentopia tower"))), encoding="utf-8")
    kb = troubleshooter.build(Path(__file__).resolve().parent.parent / "src" / "troubleshooter.html",
                              OUT / "support" / "tower-first-aid.html") // 1024
    print(f"Tower First Aid: {kb} KB")
    tpl = pages["index.html"]
    (OUT / "thanks.html").write_text(simple_page(
        tpl, "Thank you", "Thanks — we got your message.",
        "We’ll reply to the email you gave us, usually within two business days.",
        "index.html", "Back to home"), encoding="utf-8")
    (OUT / "404.html").write_text(simple_page(
        tpl, "Page not found", "We couldn’t find that page.",
        "It may have moved when we rebuilt our site. Try the menu above, or start from the home page.",
        "index.html", "Go to home page"), encoding="utf-8")
    print(f"built {len(pages) + 2} pages into {OUT}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import i18n
    if (OUT / "ja").exists():
        shutil.rmtree(OUT / "ja")
    missing = i18n.build(OUT, Path(__file__).resolve().parent.parent / "src" / "i18n" / "ja.tsv")
    if missing:
        raise SystemExit(f"{len(missing)} English texts have no Japanese yet (see above)")
    # Sitemap and robots.txt for search engines
    site = "https://www.greentopia.jp"
    names = sorted(p.name for p in OUT.glob("*.html") if p.name not in ("404.html", "thanks.html"))
    urls = []
    for n in names:
        path = "" if n == "index.html" else n
        alts = (f'<xhtml:link rel="alternate" hreflang="en" href="{site}/{path}"/>'
                f'<xhtml:link rel="alternate" hreflang="ja" href="{site}/ja/{path}"/>')
        urls += [f"<url><loc>{site}/{path}</loc>{alts}</url>", f"<url><loc>{site}/ja/{path}</loc>{alts}</url>"]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nDisallow: /_build/\nSitemap: {site}/sitemap.xml\n",
                                    encoding="utf-8")


main()
