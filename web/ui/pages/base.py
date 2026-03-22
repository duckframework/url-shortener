"""
BasePage — shared page shell for all Snip pages.

Handles global CSS, fonts, and all SEO in one place so every page
inherits it automatically. Subclasses override the class-level
constants and get_json_ld() for per-page customisation.
"""
import json

from duck.shortcuts import resolve, static
from duck.utils.urlcrack import URL
from duck.html.components.page import Page
from duck.html.components.style import Style


DUCK_HOMEPAGE = "https://duckframework.xyz"
DONATE_URL = f"{DUCK_HOMEPAGE}/contribute"
SITE_NAME = "Snip"
SITE_AUTHOR = "Duck Framework"

GLOBAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@400;500;600;700&display=swap');

:root {
    --bg:        #070809;
    --surface:   #0e1012;
    --border:    rgba(255,255,255,0.07);
    --accent:    #00ff87;
    --accent2:   #0dffe9;
    --indigo:    #6366f1;
    --red:       #ff4d6d;
    --text:      #f0f0f0;
    --muted:     rgba(240,240,240,0.38);
    --mono:      'DM Mono', monospace;
    --serif:     'Instrument Serif', serif;
    --sans:      'DM Sans', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
}

body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.022) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.022) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

body::after {
    content: '';
    position: fixed;
    top: -200px;
    left: 50%;
    transform: translateX(-50%);
    width: 700px;
    height: 500px;
    background: radial-gradient(ellipse, rgba(0,255,135,0.06) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

input, button, a { font-family: var(--sans); }
input::placeholder { color: rgba(255,255,255,0.22); }
input:focus {
    outline: none;
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,255,135,0.1);
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 99px; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}

.fade-up          { animation: fadeUp 0.55s ease both; }
.fade-up.delay-1  { animation-delay: 0.1s; }
.fade-up.delay-2  { animation-delay: 0.2s; }
.fade-up.delay-3  { animation-delay: 0.3s; }
.fade-up.delay-4  { animation-delay: 0.45s; }
.fade-up.delay-5  { animation-delay: 0.6s; }

.snip-nav {
    position: relative; z-index: 10;
    display: flex; align-items: center; justify-content: space-between;
    padding: 20px 36px;
    border-bottom: 1px solid var(--border);
}
.snip-logo {
    font-family: var(--mono); font-size: 1.05rem; font-weight: 500;
    color: var(--text); text-decoration: none;
    display: flex; align-items: center; gap: 8px;
}
.snip-logo-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--accent);
    animation: pulse-dot 2s ease-in-out infinite;
}
.nav-links { display: flex; align-items: center; gap: 6px; }
.nav-link {
    font-size: 0.8rem; font-weight: 500; color: var(--muted);
    text-decoration: none; padding: 6px 12px; border-radius: 8px;
    transition: color 0.15s, background 0.15s; letter-spacing: 0.02em;
}
.nav-link:hover { color: var(--text); background: rgba(255,255,255,0.05); }
.nav-donate {
    font-size: 0.8rem; font-weight: 600; color: #fff;
    text-decoration: none; padding: 7px 16px; border-radius: 8px;
    background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12);
    transition: background 0.15s, border-color 0.15s; letter-spacing: 0.02em;
    display: flex; align-items: center; gap: 6px;
}
.nav-donate:hover {
    background: rgba(255,77,109,0.12); border-color: rgba(255,77,109,0.4); color: #ff6b84;
}

.hero-kicker {
    font-family: var(--mono); font-size: 0.72rem;
    letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent);
    display: flex; align-items: center; gap: 8px;
}
.hero-kicker::before {
    content: ''; display: inline-block;
    width: 24px; height: 1px; background: var(--accent);
}
.hero-title {
    font-family: var(--serif); font-size: clamp(2.8rem, 7vw, 5rem);
    font-weight: 400; line-height: 1.05; letter-spacing: -0.02em; color: #fff;
}
.hero-title em {
    font-style: italic;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent));
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    animation: shimmer 4s linear infinite;
}

.stat-card {
    display: flex; flex-direction: column; align-items: flex-start;
    gap: 2px; padding: 18px 24px; border-radius: 12px;
    background: var(--surface); border: 1px solid var(--border);
    min-width: 140px; position: relative; overflow: hidden;
}
.stat-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,135,0.4), transparent);
}

.form-card {
    width: 100%; max-width: 640px;
    border-radius: 18px; background: var(--surface); border: 1px solid var(--border);
    overflow: hidden;
}
.form-card-header {
    padding: 14px 22px; border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 8px;
}
.form-card-dot { width: 10px; height: 10px; border-radius: 50%; }
.form-card-body { padding: 22px; }

.result-line {
    display: flex; align-items: center; gap: 4px;
    font-family: var(--mono); font-size: 0.72rem;
    color: var(--muted); letter-spacing: 0.05em;
    margin-bottom: 8px; text-transform: uppercase;
}
.result-line::before { content: '>'; color: var(--accent); font-weight: 600; }

.snip-footer {
    text-align: center; padding: 32px 20px 40px;
    border-top: 1px solid var(--border); position: relative; z-index: 1;
}
.footer-built {
    font-size: 0.78rem; color: var(--muted);
    display: flex; align-items: center; justify-content: center; gap: 6px; flex-wrap: wrap;
}
.footer-built a { color: var(--text); text-decoration: none; font-weight: 600; transition: color 0.15s; }
.footer-built a:hover { color: var(--accent); }
.footer-sep { opacity: 0.3; }

@media (max-width: 600px) {
    .snip-nav { padding: 16px 20px; }
    .nav-link { display: none; }
}
"""


class BasePage(Page):
    """
    Base page for all Snip pages.

    Injects global styles and configures all SEO metadata using Duck's
    built-in SEO methods. Subclasses override PAGE_* constants and
    get_json_ld() for per-page customisation.
    """

    # Override in subclasses for per-page SEO
    PAGE_TITLE = "Snip — Free URL Shortener | Powered by Duck Framework"
    PAGE_DESCRIPTION = (
        "Snip turns long, messy URLs into clean short links in one click. "
        "No sign-up. No tracking. Pure Python — zero JavaScript."
    )
    PAGE_TYPE = "website"
    PAGE_IMAGE = static("images/og-image.png")
    PAGE_KEYWORDS    = [
        "url shortener", "free url shortener", "link shortener",
        "short link", "shorten url", "duck framework",
        "python web framework", "no javascript", "snip",
    ]
    
    def on_create(self):
        super().on_create()

        # Resolve absolute page URL from current request path
        self._path = getattr(self.request, "path", "/")
        self._home_url = resolve("home", absolute=True)
        self._page_url = URL(self._home_url).join(self._path).to_str()
        
        # Inject styles plus SEO
        self.inject_styles()
        self.inject_seo()

    def inject_styles(self):
        """
        Injects the global CSS stylesheet shared across all pages.
        """
        self.add_to_head(Style(inner_html=GLOBAL_CSS))

    def inject_seo(self):
        """
        Configures all SEO metadata using Duck's built-in SEO methods.
        """
        # Core meta
        self.set_lang("en")
        self.set_title(self.PAGE_TITLE)
        self.set_description(self.PAGE_DESCRIPTION)
        self.set_author(SITE_AUTHOR)
        self.set_robots("index, follow")
        self.set_keywords(self.PAGE_KEYWORDS)

        # Canonical URL
        self.set_canonical(self._page_url)

        # Open Graph
        self.set_opengraph(
            title=self.PAGE_TITLE,
            description=self.PAGE_DESCRIPTION,
            url=self._page_url,
            image=self.PAGE_IMAGE,
            type=self.PAGE_TYPE,
            site_name=SITE_NAME,
        )

        # Twitter Card
        self.set_twitter_card(
            card="summary_large_image",
            title=self.PAGE_TITLE,
            description=self.PAGE_DESCRIPTION,
        )

        # JSON-LD structured data
        self.set_json_ld(self.get_json_ld())

    def get_json_ld(self) -> dict:
        """
        Returns JSON-LD structured data for this page.
        Override in subclasses for page-specific schemas.
        """
        return {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": SITE_NAME,
            "url": self._page_url,
            "description": self.PAGE_DESCRIPTION,
            "applicationCategory": "UtilitiesApplication",
            "operatingSystem": "All",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD",
            },
            "author": {
                "@type": "Organization",
                "name": "Duck Framework",
                "url": DUCK_HOMEPAGE,
            },
        }
