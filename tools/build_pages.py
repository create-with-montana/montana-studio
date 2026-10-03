# Builds the shared footer into index.html and generates the About, Privacy,
# Terms and Disclaimers pages. Edit FOOTER, ABOUT or tools/legal/*.md, then run:
#   python3 tools/build_pages.py
import re, html, json, pathlib
REPO = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).resolve().parent / 'legal'

FOOTER = '''<!-- ===== FOOTER ===== -->
<footer class="site-foot">
  <div class="foot-top">
    <div class="foot-brand">
      <a href="/" class="foot-logo"><img src="/images/logo-light.png" alt="Montana Studio" width="150" height="40"></a>
      <p>Montana Studio is a brand management studio based in Ontario, Canada. Our team looks after social media, website design and development, SEO and GEO, Shopify and e-commerce, email marketing and the systems behind them, for founders across Canada and beyond.</p>
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
        <a href="mailto:montana@createwithmontana.com">montana@<wbr>createwithmontana.com</a><br>
        Ontario, Canada
      </address>
      <a class="btn" href="/#inquire">Inquire</a>
    </div>
  </div>
  <div class="foot-base">
    <span>&copy; 2026 Montana Studio. All rights reserved.</span>
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
<title>{title} · Montana Studio</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#11100e">
<link rel="canonical" href="https://montanastudio.ca/{slug}">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
</head>
<body class="legal-page">
<header class="legal-bar">
  <a href="/" class="foot-logo"><img src="/images/logo-light.png" alt="Montana Studio" width="150" height="40"></a>
  <a class="under" href="/">Back to the studio</a>
</header>
<main class="legal">
  <h1>{title}</h1>
{md(body_md)}
</main>
{FOOTER}
</body>
</html>
'''

pages = [
  ('privacy', 'Privacy Policy', 'How Montana Studio collects, uses and protects your personal information.', 'privacy.md'),
  ('terms-and-conditions', 'Terms &amp; Conditions', 'The terms that govern use of the Montana Studio website, services and products.', 'terms.md'),
  ('disclaimers', 'Disclaimers', 'Disclaimers for the content, services and products offered by Montana Studio.', 'disclaimers.md'),
]
for slug, title, desc, src in pages:
    (REPO / slug).mkdir(exist_ok=True); (REPO / slug / 'index.html').write_text(page(slug, title, desc, (HERE / src).read_text()))

ABOUT = f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>About · Montana Studio</title>
<meta name="description" content="Montana Studio is a boutique business studio in Ontario, Canada, helping founders build businesses that are beautiful, efficient and built to scale, across strategy, operations, systems and brand.">
<meta name="theme-color" content="#11100e">
<link rel="canonical" href="https://montanastudio.ca/about">
<meta property="og:title" content="About · Montana Studio">
<meta property="og:image" content="/images/og.jpg">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<header class="page-head">
  <div class="nav">
    <a class="wordmark" href="/"><img src="/images/logo-light.png" alt="Montana Studio"></a>
    <ul>
      <li><a href="/#services">Services</a></li>
      <li><a href="/#studio">The Studio</a></li>
      <li><a href="/about" aria-current="page">About</a></li>
      <li><a href="/#testimonials">Testimonials</a></li>
      <li><a href="/#inquire">Inquire</a></li>
    </ul>
    <span class="menu">Menu</span>
  </div>
</header>
<main>
  <!-- ===== ABOUT THE STUDIO ===== -->
  <section class="about-intro">
    <span class="cap">About the studio</span>
    <h1>Strategy. Operations. <i>Brand.</i></h1>
    <div class="body">
      <p>Montana Studio is a boutique business studio helping founders build businesses that are beautiful, efficient, and built to scale.</p>
      <p>Our work lives at the intersection of strategy, operations, systems, and brand, because lasting growth doesn’t come from one area alone. It happens when every part of the business works together.</p>
      <p>From refining your brand and designing a high-converting website to streamlining operations, implementing systems, leading projects, and optimizing the client experience, we become a trusted partner behind the scenes.</p>
      <p class="motto">Driven by integrity. Rooted in kindness. Committed to your growth.</p>
    </div>
  </section>

  <!-- ===== MEET THE FOUNDER ===== -->
  <section class="founder" id="founder">
    <div class="photo" role="img" aria-label="Montana, founder of Montana Studio"></div>
    <div class="text">
      <span class="cap">Meet the founder</span>
      <h2>Mon<i>tana</i></h2>
      <p class="role">Founder &amp; Studio Director</p>
      <p>Montana’s bio is coming soon.</p>
    </div>
  </section>

  <!-- ===== ABOUT CTA ===== -->
  <section class="about-cta">
    <h2>Let Us Look After <i>It.</i></h2>
    <div class="actions"><a class="btn" href="/#inquire">Inquire</a></div>
  </section>
</main>
{FOOTER}
</body>
</html>
'''
(REPO / 'about').mkdir(exist_ok=True); (REPO / 'about' / 'index.html').write_text(ABOUT)

# Homepage footer
idx = REPO / 'index.html'
s = idx.read_text()
a = s.index('<!-- ===== FOOTER ===== -->'); b = s.index('</footer>') + len('</footer>')
s = s[:a] + FOOTER + s[b:]
idx.write_text(s)
print('ok')
