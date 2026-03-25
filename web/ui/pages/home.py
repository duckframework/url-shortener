"""
HomePage — Snip URL Shortener landing page.

Inherits all styles, SEO, and structured data from BasePage.
Only defines what is unique to this page.
"""
from duck.html.components.container import FlexContainer
from duck.html.components.paragraph import Paragraph
from duck.html.components import to_component

from web.ui.pages.base import BasePage, DUCK_HOMEPAGE, DONATE_URL
from web.ui.components.shorten_form import ShortenForm
from web.ui.components.stats_bar import StatsBar


class HomePage(BasePage):
    """
    Landing page — inherits all SEO and global styles from BasePage.
    """
    PAGE_TITLE  = "Snip — Free URL Shortener | Powered by Duck Framework"
    PAGE_DESCRIPTION = (
        "Snip turns long, messy URLs into clean short links in one click. "
        "No sign-up. No tracking. Pure Python — zero JavaScript."
    )
    PAGE_KEYWORDS    = [
        "url shortener", "free url shortener", "link shortener",
        "short link", "shorten url", "snip", "duck framework",
        "python url shortener", "no javascript url shortener",
        "open source url shortener", "fast link shortener",
    ]

    def on_create(self):
        # BasePage.on_create handles styles + all SEO
        super().on_create()
        self.build_page()

    def get_json_ld(self) -> dict:
        """
        Homepage JSON-LD — WebApplication with a CreateAction so Google
        understands the primary action is creating a short URL.
        """
        base_json_ld = super().get_json_ld().copy()
        base_json_ld.update({
            "potentialAction": {
                "@type": "CreateAction",
                "target": self._page_url,
                "name": "Shorten a URL",
            },
        })
        return base_json_ld

    def build_page(self):
        """
        Assembles the full page layout inside a min-height wrapper.
        """
        wrapper = FlexContainer(
            style={
                "flex-direction": "column",
                "min-height": "100vh",
                "position": "relative",
                "z-index": "1",
            },
        )
        
        # Build page components
        self.build_nav(wrapper)
        self.build_main(wrapper)
        self.build_footer(wrapper)
        self.add_to_body(wrapper)

    def build_nav(self, parent: FlexContainer):
        """
        Top nav — logo, Duck Framework link, donate button.
        """
        nav = to_component("", "nav", no_closing_tag=False)
        nav.klass = "snip-nav fade-up"
        nav.props["aria-label"] = "Main navigation"

        # Logo
        logo = to_component("", "a", no_closing_tag=False)
        logo.klass = "snip-logo"
        logo.props.update({"href": "/", "aria-label": "Snip home"})

        dot = to_component("", "span", no_closing_tag=False)
        dot.klass = "snip-logo-dot"
        dot.props["aria-hidden"] = "true"

        name = to_component("snip/", "span", no_closing_tag=False)
        logo.add_children([dot, name])

        # Nav links
        links = to_component("", "div", no_closing_tag=False)
        links.klass = "nav-links"

        duck_link = to_component("Duck Framework", "a", no_closing_tag=False)
        duck_link.klass = "nav-link"
        duck_link.props.update({
            "href": DUCK_HOMEPAGE,
            "target": "_blank",
            "rel": "noopener noreferrer",
            "aria-label": "Visit Duck Framework website",
        })

        donate_link = to_component("&#9829; Donate", "a", no_closing_tag=False)
        donate_link.klass = "nav-donate"
        donate_link.props.update({
            "href": DONATE_URL,
            "target": "_blank",
            "rel": "noopener noreferrer",
            "aria-label": "Support Snip on Patreon",
        })

        links.add_children([duck_link, donate_link])
        nav.add_children([logo, links])
        parent.add_child(nav)

    def build_main(self, parent: FlexContainer):
        """
        Main content — hero, live stats, and the shorten form.
        """
        main = to_component("", "main", no_closing_tag=False)
        main.props["id"] = "main-content"

        inner = FlexContainer(
            style={
                "flex-direction": "column",
                "align-items": "center",
                "flex": "1",
                "padding": "64px 20px 48px",
                "gap": "0",
                "min-height": "90vh",
            },
        )
        
        # Build main content.
        self.build_hero(inner)
        self.build_stats(inner)
        self.build_form(inner)
        main.add_child(inner)
        parent.add_child(main)

    def build_hero(self, parent: FlexContainer):
        """
        Hero section — kicker, serif headline with shimmer accent, tagline.
        """
        hero = FlexContainer(
            style={
                "flex-direction": "column",
                "align-items": "center",
                "text-align": "center",
                "gap": "20px",
                "max-width": "680px",
                "margin-bottom": "48px",
            },
        )

        # Kicker — decorative, hidden from screen readers
        kicker = to_component("Built with Duck Framework", "p", no_closing_tag=False)
        kicker.klass = "hero-kicker fade-up"
        kicker.props["aria-hidden"] = "true"

        # H1 — primary SEO heading
        title = to_component(
            "Shorten URLs.<br><em>Instantly.</em>",
            "h1",
            no_closing_tag=False,
        )
        title.klass = "hero-title fade-up delay-1"

        # Tagline
        tagline = Paragraph(
            inner_html=(
                "Paste any long URL and get a clean, shareable short link in one click. "
                "No sign-up. No tracking. Pure Python — zero JavaScript."
            )
        )
        tagline.klass = "fade-up delay-2"
        tagline.style.update({
            "font-size": "1rem",
            "color": "var(--muted)",
            "max-width": "460px",
            "line-height": "1.7",
            "margin": "0",
        })

        hero.add_children([kicker, title, tagline])
        parent.add_child(hero)

    def build_stats(self, parent: FlexContainer):
        """
        Live stats — total links shortened and total clicks, refreshes on use.
        """
        self.stats = StatsBar()
        parent.add_child(self.stats)

    def build_form(self, parent: FlexContainer):
        """
        ShortenForm inside a macOS-style window chrome card.
        """
        # Card wrapper
        card = to_component("", "div", no_closing_tag=False)
        card.klass = "form-card fade-up delay-4"

        # Window chrome dots — decorative
        header = to_component("", "div", no_closing_tag=False)
        header.klass = "form-card-header"
        header.props["aria-hidden"] = "true"

        for color in ["#ff5f57", "#febc2e", "#28c840"]:
            dot = to_component("", "span", no_closing_tag=False)
            dot.klass = "form-card-dot"
            dot.style["background"] = color
            header.add_child(dot)

        label = to_component("snip &mdash; url shortener", "span", no_closing_tag=False)
        label.style.update({
            "font-family": "var(--mono)",
            "font-size": "0.7rem",
            "color": "var(--muted)",
            "margin-left": "8px",
            "letter-spacing": "0.05em",
        })
        header.add_child(label)

        # Form body
        body = to_component("", "div", no_closing_tag=False)
        body.klass = "form-card-body"

        self.form = ShortenForm(on_shortened=self.stats.refresh, stats_bar=self.stats)
        body.add_child(self.form)

        card.add_children([header, body])

        wrapper = FlexContainer(
            style={
                "width": "100%",
                "max-width": "640px",
                "margin-top": "36px",
            },
        )
        wrapper.add_child(card)
        parent.add_child(wrapper)

    def build_footer(self, parent: FlexContainer):
        """
        Footer — Duck Framework attribution and donate link.
        """
        footer = to_component("", "footer", no_closing_tag=False)
        footer.klass = "snip-footer"
        footer.props["aria-label"] = "Site footer"

        inner = to_component(
            f'Built with '
            f'<a href="{DUCK_HOMEPAGE}" target="_blank" rel="noopener noreferrer">Duck Framework</a>'
            f'<span class="footer-sep" aria-hidden="true"> · </span>'
            f'<a href="{DONATE_URL}" target="_blank" rel="noopener noreferrer">&#9829; Support the project</a>'
            f'<span class="footer-sep" aria-hidden="true"> · </span>'
            f'Open source. Free forever.',
            "div",
            no_closing_tag=False,
        )
        inner.klass = "footer-built"
        
        # Configure footer and add it to its parent.
        footer.add_child(inner)
        parent.add_child(footer)
