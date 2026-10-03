# Builds the shared footer into index.html and generates the About, Privacy,
# Terms and Disclaimers pages. Edit FOOTER, ABOUT or tools/legal/*.md, then run:
#   python3 tools/build_pages.py
import re, html, json, pathlib
REPO = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).resolve().parent / 'legal'

def header(current=''):
    """Glass header with the full menu, shared by every page except the homepage."""
    links = [('/#services', 'Services'), ('/#studio', 'The Studio'), ('/about', 'About'), ('/#testimonials', 'Testimonials'), ('/#inquire', 'Inquire')]
    items = '\n'.join(f'      <li><a href="{h}"' + (' aria-current="page"' if h == current else '') + f'>{t}</a></li>' for h, t in links)
    return f'''<header class="glass-head">
  <div class="nav">
    <a class="wordmark" href="/"><img src="/images/logo-light.png" alt="MONTANA Studio"></a>
    <ul>
{items}
    </ul>
    <span class="menu">Menu</span>
  </div>
</header>'''

FOOTER = '''<!-- ===== FOOTER ===== -->
<footer class="site-foot">
  <div class="foot-top">
    <div class="foot-brand">
      <a href="/" class="foot-logo"><img src="/images/logo-light.png" alt="MONTANA Studio" width="150" height="40"></a>
      <p>MONTANA Studio is a brand management studio based in Ontario, Canada. Our team looks after social media, website design and development, SEO and GEO, Shopify and e-commerce, email marketing and the systems behind them, for founders across Canada and beyond.</p>
    </div>
    <nav class="foot-col" aria-label="Services">
      <h2 class="cap">Services</h2>
      <ul>
        <li><a href="/#s-social">Social Media Management</a></li>
        <li><a href="/#s-web">Website Design &amp; Development</a></li>
        <li><a href="/#s-seo">SEO &amp; GEO</a></li>
        <li><a href="/#s-shop">E-Commerce &amp; Shopify</a></li>
        <li><a href="/#s-email">Email &amp; Campaign Management</a></li>
        <li><a href="/#s-systems">Digital Presence Management</a></li>
      </ul>
    </nav>
    <nav class="foot-col" aria-label="Studio">
      <h2 class="cap">Studio</h2>
      <ul>
        <li><a href="/#studio">The Studio</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/#testimonials">Testimonials</a></li>
      </ul>
    </nav>
    <div class="foot-col">
      <h2 class="cap">Contact</h2>
      <address>
        <a href="mailto:montana@createwithmontana.com">montana@<wbr>createwithmontana.com</a>
      </address>
      <a class="btn" href="/#inquire">Inquire</a>
    </div>
  </div>
  <div class="foot-base">
    <span>&copy; 2026 MONTANA Studio. All rights reserved.</span>
    <nav aria-label="Legal"><a href="/privacy">Privacy</a><a href="/terms-and-conditions">Terms &amp; Conditions</a><a href="/disclaimers">Disclaimers</a></nav>
  </div>
</footer>'''

def md(text):
    def inline(s):
        s = html.escape(s, quote=False)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
        return s
    out, lst = [], False
    for block in text.strip().split('\n\n'):
        lines = block.split('\n')
        if all(l.startswith('- ') for l in lines):
            out.append('<ul>' + ''.join(f'<li>{inline(l[2:])}</li>' for l in lines) + '</ul>')
        elif block.startswith('## '):
            out.append(f'<h2>{inline(block[3:])}</h2>')
        else:
            out.append(f'<p>{inline(" ".join(lines))}</p>')
    return '\n'.join(out)

def page(slug, title, desc, body_md):
    return f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · MONTANA Studio</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#11100e">
<link rel="canonical" href="https://montanastudio.ca/{slug}">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
</head>
<body class="legal-page">
{header()}
<main class="legal">
  <h1>{title}</h1>
{md(body_md)}
</main>
{FOOTER}
</body>
</html>
'''

pages = [
  ('privacy', 'Privacy Policy', 'How MONTANA Studio collects, uses and protects your personal information.', 'privacy.md'),
  ('terms-and-conditions', 'Terms &amp; Conditions', 'The terms that govern use of the MONTANA Studio website, services and products.', 'terms.md'),
  ('disclaimers', 'Disclaimers', 'Disclaimers for the content, services and products offered by MONTANA Studio.', 'disclaimers.md'),
]
for slug, title, desc, src in pages:
    (REPO / slug).mkdir(exist_ok=True); (REPO / slug / 'index.html').write_text(page(slug, title, desc, (HERE / src).read_text()))

# About page FAQ: written answer-first so search engines and AI assistants can quote
# each answer on its own. The same list feeds the FAQPage structured data.
FAQ = [
  ('What does MONTANA Studio do?',
   'MONTANA Studio is a brand management studio based in Ontario, Canada. Our team looks after social media management, website design and development, SEO and GEO, Shopify and e-commerce, email and campaign management, and digital presence management, including courses, lead funnels, CRMs and workflows. You work with one full team through one point of contact.'),
  ('Who do you work with?',
   'We work with founders, small business owners and entrepreneurs who are ready to grow and want a partner who is as invested in their business as they are. Many of our clients are service-based businesses, coaches and e-commerce brands.'),
  ('Do you only work with businesses in Ontario?',
   'No. The studio is based in Ontario, and we work with clients across Canada and beyond. Consultations and meetings take place online, so where you are has no bearing on the care you receive.'),
  ('Do I need a monthly retainer?',
   'A monthly retainer is absolutely an option, depending on the services you need. For ongoing work such as social media management, we offer retainers and packages to suit different needs. Above all, our goal is to make sure everything you need is looked after, so we take a tailored, customizable approach: project-based work for one-time needs, and retainers for ongoing support.'),
  ('How much do your services cost?',
   'Pricing is customized to each client, so it can vary significantly with the size of the project or the scope of ongoing work. We offer both project-based pricing and monthly retainers. After your consultation, we prepare a tailored proposal with clear pricing, so you know exactly what to expect before anything begins.'),
  ('What is GEO, and why does it matter for my business?',
   'GEO, or generative engine optimization, helps your business appear in answers from AI search tools such as ChatGPT, Google AI Overviews, Gemini and Perplexity. We pair it with traditional SEO through clear, well-structured content, structured data and consistent business information, so your brand can be found and recommended wherever your clients search.'),
  ('Can you manage my social media for me?',
   'Yes. Our social media management covers strategy, content creation, scheduling, engagement, and reporting and analytics, so your accounts stay consistent and on brand while you focus on running your business.'),
  ('Do you build Shopify stores?',
   'Yes. We design and build Shopify stores, migrate existing stores to Shopify, set up products and apps, and offer ongoing store management once you launch.'),
  ('Do you offer support after my website launches?',
   'Yes. We offer hosting and monthly care, along with ongoing SEO, GEO and content support, so your website keeps performing long after launch.'),
  ('What happens after I send an inquiry?',
   'We reply within two business days to book a consultation. From there we begin with discovery, a deep dive into your business, goals and ideal client, then shape a strategy, design and develop the work, and set up the systems behind it.'),
]
FAQ_HTML = '\n'.join(f'      <details class="qa"><summary><h3>{html.escape(q)}</h3></summary><p>{html.escape(a)}</p></details>' for q, a in FAQ)
FAQ_LD = json.dumps({
  '@context': 'https://schema.org',
  '@graph': [
    {'@type': 'AboutPage', 'url': 'https://montanastudio.ca/about', 'name': 'About MONTANA Studio',
     'about': {'@type': 'ProfessionalService', 'name': 'MONTANA Studio', 'url': 'https://montanastudio.ca/'},
     'mainEntity': {'@type': 'Person', 'name': 'Montana Fisher-Shotton', 'jobTitle': 'Founder & Studio Director',
                    'image': 'https://montanastudio.ca/images/montana.jpg',
                    'worksFor': {'@type': 'ProfessionalService', 'name': 'MONTANA Studio'}}},
    {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]},
  ]}, indent=1, ensure_ascii=False)

# The homepage inquiry section, repeated at the foot of the About page
_home = (REPO / 'index.html').read_text()
INQUIRE = _home[_home.index('<!-- ===== INQUIRE ===== -->'):_home.index('</section>', _home.index('id="inquire"')) + len('</section>')]

ABOUT = f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>About · MONTANA Studio</title>
<meta name="description" content="MONTANA Studio is a boutique business studio in Ontario, Canada, helping founders build businesses that are beautiful, efficient and built to scale, across strategy, operations, systems and brand.">
<meta name="theme-color" content="#11100e">
<link rel="canonical" href="https://montanastudio.ca/about">
<meta property="og:title" content="About · MONTANA Studio">
<meta property="og:image" content="/images/og.jpg">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">
{FAQ_LD}
</script>
</head>
<body>
{header('/about')}
<main>
  <!-- ===== ABOUT THE STUDIO ===== -->
  <section class="about-intro">
    <span class="cap">About the studio</span>
    <h1>Strategy. Operations. <i>Brand.</i></h1>
    <div class="body">
      <p>MONTANA Studio is a boutique business studio helping founders build businesses that are beautiful, efficient, and built to scale.</p>
      <p>Our work lives at the intersection of strategy, operations, systems, and brand, because lasting growth doesn’t come from one area alone. It happens when every part of the business works together.</p>
      <p>From refining your brand and designing a high-converting website to streamlining operations, implementing systems, leading projects, and optimizing the client experience, we become a trusted partner behind the scenes.</p>
      <p class="motto">Driven by integrity. Rooted in kindness. Committed to your growth.</p>
    </div>
  </section>

  <!-- ===== MEET THE FOUNDER ===== -->
  <section class="founder" id="founder">
    <div class="photo" role="img" aria-label="Montana, founder of MONTANA Studio"></div>
    <div class="text">
      <span class="cap">Meet the founder</span>
      <h2>Montana</h2>
      <p class="role">Founder &amp; Studio Director</p>
      <div class="bio">
        <p>Hi, I’m Montana — designer, strategist, and the heart behind MONTANA Studio. I’ve always believed that good design goes beyond how something looks — it’s about how it works, how it feels, and how it supports your bigger vision.</p>
        <p>Before launching this studio, I spent years as a Director of Operations, helping businesses build the systems and structure that keep things running behind the scenes. That experience taught me something important: a beautiful brand without a strong foundation can only go so far. That’s why my approach blends intentional design with strategic thinking, so your brand not only shows up beautifully, but functions with clarity and purpose.</p>
        <p>I work with passionate small business owners and entrepreneurs who are ready to level up and want a partner who’s as invested in their growth as they are. I’m here to make the process feel less overwhelming, more aligned, and honestly… more fun.</p>
        <p>At the core, I’m driven, no-nonsense, and deeply kind. I care about doing great work, treating people right, and building businesses that feel good from the inside out.</p>
      </div>
    </div>
  </section>

  <!-- ===== FAQ ===== -->
  <section class="faq" id="faq" aria-labelledby="faq-title">
    <div class="faq-head">
      <span class="cap">Questions</span>
      <h2 id="faq-title">Frequently Asked <i>Questions</i></h2>
      <p>Anything else on your mind? Send it with your inquiry below.</p>
    </div>
    <div class="faq-list">
{FAQ_HTML}
    </div>
  </section>

{INQUIRE}
</main>
{FOOTER}
<script src="/cutout.js" defer></script>
<script src="/inquire.js" defer></script>
</body>
</html>
'''
(REPO / 'about').mkdir(exist_ok=True); (REPO / 'about' / 'index.html').write_text(ABOUT)

# Thank-you page: where the inquiry form lands after sending. Kept out of search results.
THANKS = f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Thank You · MONTANA Studio</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#11100e">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
{header()}
<main>
  <section class="inquire thanks">
    <div class="pane">
      <h1 class="look"><span class="above"><span class="over">Thank</span><span class="cut dip" aria-hidden="true">Thank</span></span> <span class="cut"><i>You.</i></span></h1>
      <span class="cap">We’ve received your inquiry</span>
      <p>Thank you so much for reaching out. We will be in touch within 24 to 48 hours to book your consultation, and we’re looking forward to connecting with you.</p>
      <div class="send"><a class="btn" href="/">Back to the studio</a></div>
    </div>
  </section>
</main>
{FOOTER}
<script src="/cutout.js" defer></script>
</body>
</html>
'''
(REPO / 'thank-you').mkdir(exist_ok=True); (REPO / 'thank-you' / 'index.html').write_text(THANKS)

# Homepage footer
idx = REPO / 'index.html'
s = idx.read_text()
a = s.index('<!-- ===== FOOTER ===== -->'); b = s.index('</footer>') + len('</footer>')
s = s[:a] + FOOTER + s[b:]
idx.write_text(s)
print('ok')
