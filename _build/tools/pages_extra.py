"""Hand-written page bodies and content for pages beyond the v13 prototype.

Home Towers (lease plans from the Tower Lease Options flyer), What You Can Grow (from the
Tower Varieties v2 and Autumn Recommendations flyers) and Customer Support.
"""
SEEDLING_FORM = "https://forms.gle/aPXLKN9J2pFvpjF18"

SERVICE_AREA = (
    '<div class="area-box"><p><strong>Service area:</strong> Shinjuku, Shibuya, Minato, and Setagaya wards.</p>'
    '<p>We also visit parts of Shinagawa, Meguro, Chiyoda, Toshima, and Koto wards near our partner schools. '
    'Coverage there is limited, so <a href="contact.html?interest=home-tower">contact us</a> to check your address.</p></div>')

HOME_TOWERS_MAIN = f'''<main class="site-main"><section class="hero"><div class="hero-copy"><span class="eyebrow">Home Towers</span>
<h1>Grow fresh food at home, indoors or outdoors.</h1>
<p>Lease a tower, grow your own food — no experience needed.</p>
<div class="hero-actions"><a class="button cta-orange" href="contact.html?interest=home-tower">Start a 3-month trial</a></div></div>
HERO_PLACEHOLDER</section>

<section class="content-section"><span class="eyebrow">Your tower</span><h2>Overview</h2>
<div class="text-placeholder"><p>A hydroponic tower grows fresh greens, vegetables, herbs, and flowers right in your home — on a balcony, patio, or even in your kitchen with a grow light. No soil, no mess, and no gardening experience needed. The system runs automatically on a pump and timer; you add water and nutrients, plant your seedlings, and harvest when they are ready. It is a living kitchen garden that fits in a space smaller than one square meter.</p>
<p>Two sizes: a 5-pot tower for indoor or outdoor use, and a larger 7-pot tower for outdoor spaces.</p></div>
<div class="inline-actions"><a class="button secondary" href="grow.html">See what you can grow</a></div></section>

<section class="content-section" id="plans"><span class="eyebrow">Investment</span><h2>Lease plans</h2>
<p class="section-intro">Everything you need to grow fresh vegetables, edible flowers, and leafy greens year-round, indoors or out. All prices include consumption tax.</p>
<div class="plan-trial"><div class="plan-head"><span class="event-type">Step 1 · Everyone starts here</span><h3>First 3 months — trial period <span class="price">¥13,000 / month</span></h3></div>
<p>Includes the hydroponic tower (with optional LED lights for indoor growing), installation and setup, a free starter set, three months of nutrient solution and pH buffers, twice-monthly maintenance visits (water, nutrients and pH, seedling replenishment, tower cleaning), and remote support. During these three months we also teach you how to care for the tower yourself.</p></div>
<h3 class="plan-step">Step 2 · From month 4, choose your plan</h3>
<div class="card-grid plan-grid">
<div class="feature-card plan-card"><span class="event-type">Self-Care</span><h3><span class="price">¥11,000 / month</span></h3><p>The tower, installation and setup, and remote support. You handle daily care and tower cleaning yourself — we teach you how during the trial. Nutrient and pH refills are available separately.</p></div>
<div class="feature-card plan-card"><span class="event-type">Monthly Visit</span><h3><span class="price">¥15,000 / month</span></h3><p>Everything in Self-Care, plus one maintenance visit each month (water, nutrients and pH, seedling replenishment, tower cleaning).</p></div>
<div class="feature-card plan-card plan-featured"><span class="event-type">Weekly Visit · Fully managed</span><h3><span class="price">¥19,000 / month</span></h3><p>Everything above, plus weekly maintenance visits. From planting to harvest, leave it all to us. Recommended for restaurants, avid veggie eaters, and anyone who just wants to enjoy the harvest.</p></div>
</div>
<ul class="content-list plan-notes">
<li>All plans are flat monthly rates, including visit and parking costs — no additional fees.</li>
<li>Tower cleaning may include swapping your tower for a freshly cleaned one when needed, at no extra charge.</li>
<li>At the end of your lease, you can renew or return the tower.</li>
</ul>
{SERVICE_AREA}</section>

<section class="content-section"><span class="eyebrow">Extras</span><h2>Add-ons</h2>
<div class="card-grid">
<div class="feature-card"><span class="event-type">One-off</span><h3>Single maintenance visit <span class="price">¥3,500</span></h3><p>For Self-Care customers, or extra visits beyond your plan.</p></div>
<div class="feature-card"><span class="event-type">One-off</span><h3>Tower deep cleaning <span class="price">¥5,000</span></h3><p>Recommended every 2–3 months or at replanting. Included at no charge in the visit plans; Self-Care customers can do it themselves or book it as a one-off.</p></div>
<div class="feature-card"><span class="event-type">Anytime</span><h3>Seedlings <span class="price">¥200–300 / cube</span></h3><p>Priced per rockwool cube, which fills one planting port. Each cube usually holds 2–4 plants, depending on the variety.</p></div>
</div></section>

<section class="content-section"><span class="eyebrow">Get started</span><h2>Next steps</h2>
<div class="card-grid">
<a class="feature-card" href="contact.html?interest=home-tower"><h3>Start a trial</h3><p>Tell us about your space and we’ll recommend the right tower.</p></a>
<a class="feature-card" href="{SEEDLING_FORM}" target="_blank" rel="noopener"><h3>Order seedlings</h3><p>Order seedlings through our Google Form.</p></a>
<a class="feature-card" href="support.html"><h3>Already a customer?</h3><p>Troubleshooting, seedling orders, and visit requests.</p></a>
</div></section>
</main>'''

# ---------- What you can grow ----------
# (English name, outdoor-only)
VARIETIES = [
    ("Leafy greens", [("Romaine lettuce", 0), ("Chima sanchu", 0), ("Sunny / red leaf lettuce", 0),
                      ("Butterhead lettuce", 0), ("Frilled lettuce", 0), ("Arugula", 0), ("Kale (many varieties)", 0),
                      ("Mizuna", 0), ("Komatsuna", 0), ("Wasabina", 0), ("Watercress", 0), ("Corn salad / mâche", 0),
                      ("Spinach", 0), ("Swiss chard", 0), ("Shungiku", 0), ("Italian shungiku", 0)]),
    ("Fruiting vegetables", [("Mini tomato", 1), ("Cucumber", 1), ("Bell pepper", 1), ("Shishito pepper", 1),
                             ("Paprika", 1), ("Eggplant", 1), ("Okra", 1), ("Zucchini", 1), ("Bitter melon", 1),
                             ("Bush bean", 1), ("Pole bean", 1), ("Snap pea", 1), ("Snow pea", 1), ("Edamame", 1),
                             ("Pumpkin (kabocha)", 1), ("Mini watermelon", 1), ("Melon", 1), ("Lemon cucumber", 1)]),
    ("Herbs", [("Sweet basil", 0), ("Lemon basil", 0), ("Cinnamon basil", 0), ("Purple basil", 0), ("Green shiso", 0),
               ("Red shiso", 0), ("Spearmint", 0), ("Peppermint", 0), ("Oregano", 0), ("Thyme", 0), ("Rosemary", 0),
               ("Sage", 0), ("Dill", 0), ("Chervil", 0), ("Chives", 0), ("Nira (garlic chives)", 0), ("Cilantro", 0),
               ("Italian parsley", 0), ("Curled parsley", 0), ("Lemon balm", 0), ("Chamomile", 0),
               ("Sweet marjoram", 0), ("Stevia", 0), ("Catmint", 0), ("Green onion", 0)]),
    ("Edible flowers", [("Nasturtium", 0), ("Viola", 0), ("Pansy", 0), ("Calendula", 1), ("Borage", 1),
                        ("Cornflower", 1), ("Dianthus", 0), ("Snapdragon", 0), ("Marigold", 0), ("Petunia", 0)]),
    ("Ornamental flowers", [("Dwarf sunflower", 1), ("Zinnia", 1), ("Morning glory", 1), ("Sweet pea", 1), ("Aster", 0),
                            ("Impatiens", 0), ("Poppy", 0), ("Salvia", 0), ("Statice", 0), ("Stock", 0),
                            ("Verbena", 0)]),
]

# (name, tip or "")
AUTUMN = [
    ("Leafy greens", [("Lettuces (all types)", ""), ("Kale (all types)", "Gets sweeter in the cold, until December"),
                      ("Arugula", ""), ("Komatsuna", ""), ("Spinach", "In season now; slow to bolt"), ("Mizuna", ""),
                      ("Wasabina", ""), ("Shungiku", ""), ("Pak choi", ""), ("Swiss chard", ""),
                      ("Corn salad / mâche", ""), ("Watercress", "")]),
    ("Herbs", [("Cilantro", "Likes the cool weather; slow to bolt"), ("Parsley", ""), ("Chives", ""),
               ("Dill", "Until early October")]),
    ("Fruiting vegetables", [("Snap pea", "Sow now for a winter to early-spring harvest; needs support"),
                             ("Snow pea", "Sow now for a winter to early-spring harvest; needs support"),
                             ("Broad (fava) bean", "Sow in autumn, overwinters; needs support")]),
    ("Edible flowers", [("Viola / pansy", "The star of winter, October to spring"),
                        ("Calendula", "Flowers through winter if it's mild"), ("Dianthus", ""),
                        ("Cornflower", "Sow in autumn, overwinters, blooms in spring"),
                        ("Nasturtium", "Until early October (frost-tender)")]),
]


def chips(items, kind):
    out = []
    for name, extra in items:
        if kind == "all":
            sun = ' <span class="sun" title="Best grown outdoors">☀</span>' if extra else ""
            out.append(f'<li>{name}{sun}</li>')
        else:
            tip = f'<small>{extra}</small>' if extra else ""
            out.append(f'<li><span>{name}</span>{tip}</li>')
    return "".join(out)


def grow_main():
    season = "".join(f'<h3>{cat}</h3><ul class="variety-list season-list">{chips(items, "season")}</ul>'
                     for cat, items in AUTUMN)
    allv = "".join(f'<h3>{cat}</h3><ul class="variety-list">{chips(items, "all")}</ul>' for cat, items in VARIETIES)
    return f'''<main class="site-main"><section class="hero"><div class="hero-copy"><span class="eyebrow">What you can grow</span>
<h1>What you can grow in a tower</h1>
<p>Leafy greens, herbs, fruiting vegetables, and flowers. Each time we replant, we suggest varieties to match the season and your taste.</p>
<div class="hero-actions"><a class="button cta-orange" href="home-towers.html#plans">See lease plans</a></div></div>
HERO_PLACEHOLDER</section>

<section class="content-section"><span class="eyebrow">Indoors or outdoors</span><h2>Where your tower lives</h2>
<div class="card-grid">
<div class="feature-card"><h3>Indoor towers</h3><p>With LED grow lights, an indoor tower can grow almost everything on this page, all year round.</p></div>
<div class="feature-card"><h3>Outdoor towers</h3><p>Plants marked <span class="sun">☀</span> need strong sunlight, so they grow best in an outdoor tower on a balcony, terrace, or rooftop. What grows well outdoors also changes with the season.</p></div>
</div></section>

<section class="content-section season-box" id="this-season"><span class="eyebrow">This season · September–December</span><h2>Autumn picks for outdoor towers</h2>
<p class="section-intro">Easy-to-grow varieties for outdoor towers in Tokyo’s autumn and early winter. Indoor towers can grow almost anything year-round.</p>
{season}
<p class="fine-print">Avoid basil, green shiso, and lemon balm outdoors at this time of year: they can’t handle the cold.</p></section>

<section class="content-section" id="varieties"><span class="eyebrow">The full list</span><h2>Some of the things you can grow</h2>
<p class="section-intro"><span class="sun">☀</span> = best grown outdoors. Needs strong light; not suited to indoor towers.</p>
{allv}
<p class="fine-print">Varieties are subject to availability, and special-order items may need extra lead time. Root crops (carrots, radishes, and so on) and heading types are not suited to tower growing. Questions? <a href="mailto:info@greentopia.jp">info@greentopia.jp</a></p></section>
</main>'''


SUPPORT_MAIN = f'''<main class="site-main"><section class="hero"><div class="hero-copy"><span class="eyebrow">Customer support</span>
<h1>Help for Greentopia growers.</h1>
<p>Already growing with us? Fix a problem, order seedlings, or book a visit, all in one place.</p></div>
HERO_PLACEHOLDER</section>

<section class="content-section"><span class="eyebrow">How can we help?</span><h2>Choose what you need</h2>
<div class="card-grid support-grid">
<a class="feature-card support-card" href="support/tower-first-aid.html"><span class="event-type">Troubleshooting</span><h3>Tower First Aid</h3><p>Step-by-step checks for wilting plants, lights, pumps, pests, and everyday care like harvesting and cleaning. Works on your phone, even offline.</p><span class="button primary">Open Tower First Aid</span></a>
<a class="feature-card support-card" href="{SEEDLING_FORM}" target="_blank" rel="noopener"><span class="event-type">Seedlings</span><h3>Order seedlings</h3><p>¥200–300 per rockwool cube, which fills one planting port. Each cube usually holds 2–4 plants, depending on the variety.</p><span class="button primary">Open the order form</span></a>
<a class="feature-card support-card" href="contact.html?interest=customer-support"><span class="event-type">Visits and supplies</span><h3>Book a visit or ask us</h3><p>Extra maintenance visit ¥3,500 · Tower deep cleaning ¥5,000 · Nutrients, pH buffers, and starter sets on request.</p><span class="button primary">Send a request</span></a>
</div></section>

<section class="content-section"><span class="eyebrow">Good to know</span><h2>Quick reference</h2>
<div class="card-grid">
<a class="feature-card" href="grow.html"><h3>What you can grow</h3><p>Varieties for indoor and outdoor towers, plus this season’s picks.</p></a>
<a class="feature-card" href="home-towers.html#plans"><h3>Lease plans</h3><p>Self-Care, Monthly Visit, and Weekly Visit plans and add-ons.</p></a>
<a class="feature-card" href="about.html"><h3>FAQ</h3><p>Answers about hydroponics, seedlings, and troubleshooting.</p></a>
</div>
<p class="fine-print">Prefer email? Write to <a href="mailto:info@greentopia.jp">info@greentopia.jp</a> and tell us your name and where your tower is.</p></section>
</main>'''

EXTRA_CSS = """
.plan-trial{margin-top:16px;padding:18px;border:1px solid var(--green);border-radius:19px;background:var(--mint)}
.plan-trial p{margin:8px 0 0;color:var(--muted)}.plan-head h3,.plan-card h3{margin:6px 0;color:var(--forest);display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px}
.plan-step{margin:22px 0 10px;color:var(--forest)}.plan-featured{border:2px solid var(--green)}
.plan-notes{margin-top:16px}.area-box{margin-top:14px;padding:14px 18px;border-radius:16px;background:#EAF3FA;color:var(--ink)}
.area-box p{margin:4px 0}.area-box a{color:var(--green);font-weight:700}
.variety-list{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 18px;padding:0;list-style:none}
.variety-list li{padding:7px 12px;border:1px solid var(--line);border-radius:999px;background:var(--mint);font-size:14px;color:var(--forest)}
.season-list li{display:flex;flex-direction:column;border-radius:14px}.season-list small{color:var(--muted);font-size:12px}
.sun{color:var(--orange)}.season-box{background:linear-gradient(135deg,#fff,var(--mint))}.content-section h3{color:var(--forest)}
.support-card{display:flex;flex-direction:column;gap:6px}.support-card .button{margin-top:auto;align-self:flex-start}
.footer-links a[href$="support.html"]{font-weight:700}
"""
