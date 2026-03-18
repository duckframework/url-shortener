"""
HomePage — URL Shortener landing page.

Layout (top → bottom):
    Hero heading + tagline
    StatsBar       — live site-wide stats
    ShortenForm    — input, button, result, error
"""
from duck.html.components.container import FlexContainer
from duck.html.components.section import Section
from duck.html.components.heading import Heading
from duck.html.components.paragraph import Paragraph
from duck.html.components.page import Page

from web.ui.components.shorten_form import ShortenForm
from web.ui.components.stats_bar import StatsBar


DUCK_HOMEPAGE = "https://duckframework.xyz"


class HomePage(Page):
    def on_create(self):
        super().on_create()
        self.set_title("Snip — Free URL Shortener")
        self.set_description(
            "Snip turns long, messy URLs into clean short links in one click. "
            "Built with Duck Framework — pure Python, no JavaScript."
        )
        self.build_page()

    # ------------------------------------------------------------------
    # Page assembly
    # ------------------------------------------------------------------

    def build_page(self):
        wrapper = self.make_wrapper()
        self.build_styles()
        self.build_hero(wrapper)
        self.build_stats(wrapper)
        self.build_form(wrapper)
        self.add_to_body(wrapper)

    def build_styles(self):
        from duck.html.components.style import Style
        
        self.global_style = Style(inner_html="""
            body {
                margin: 0;
                background: #0a0a0f;
                color: #fff;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                min-height: 100vh;
            }
            input::placeholder { color: rgba(255,255,255,0.3); }
            input:focus {
                border-color: rgba(99,102,241,0.6) !important;
                box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
            }
            * { box-sizing: border-box; }
        """)
        self.add_to_head(self.global_style)

    def make_wrapper(self) -> FlexContainer:
        """
        Centered column wrapper — everything lives inside this.
        """
        wrapper = FlexContainer()
        wrapper.style.update({
            "flex-direction": "column",
            "align-items": "center",
            "justify-content": "center",
            "min-height": "100vh",
            "padding": "40px 20px",
        })
        return wrapper

    def build_hero(self, parent: FlexContainer):
        hero = FlexContainer()
        hero.style.update({
            "flex-direction": "column",
            "align-items": "center",
            "text-align": "center",
            "gap": "12px",
            "margin-bottom": "32px",
        })

        badge = Paragraph(inner_html=f"⚡ Built with <a href='{DUCK_HOMEPAGE}' style='text-decoration:none'>Duck Framework</a>")
        badge.style.update({
            "font-size": "0.75rem",
            "color": "rgba(99,102,241,0.9)",
            "background": "rgba(99,102,241,0.1)",
            "border": "1px solid rgba(99,102,241,0.25)",
            "padding": "4px 12px",
            "border-radius": "99px",
            "letter-spacing": "0.05em",
            "margin": "0",
        })

        title = Heading("h1", text="Snip — Shorten Any URL")
        title.style.update({
            "font-size": "clamp(2rem, 5vw, 3.2rem)",
            "font-weight": "800",
            "letter-spacing": "-0.03em",
            "margin": "0",
            "background": "linear-gradient(135deg, #fff 30%, rgba(255,255,255,0.5))",
            "-webkit-background-clip": "text",
            "-webkit-text-fill-color": "transparent",
            "background-clip": "text",
        })

        tagline = Paragraph(
            inner_html=(
                "Paste a long URL. Get a clean short link. "
                "No sign-up. Pure Python — no JavaScript."
            )
        )
        tagline.style.update({
            "font-size": "1rem",
            "color": "rgba(255,255,255,0.45)",
            "max-width": "480px",
            "line-height": "1.6",
            "margin": "0",
        })

        hero.add_children([badge, title, tagline])
        parent.add_child(hero)

    def build_stats(self, parent: FlexContainer):
        self.stats = StatsBar()
        parent.add_child(self.stats)

    def build_form(self, parent: FlexContainer):
        card = FlexContainer()
        card.style.update({
            "flex-direction": "column",
            "width": "100%",
            "max-width": "600px",
            "padding": "28px 24px",
            "margin-top": "24px",
            "border-radius": "16px",
            "background": "rgba(255,255,255,0.03)",
            "border": "1px solid rgba(255,255,255,0.07)",
            "backdrop-filter": "blur(12px)",
        })

        self.form = ShortenForm(on_shortened=self.stats.refresh, stats_bar=self.stats)
        card.add_child(self.form)
        parent.add_child(card)
