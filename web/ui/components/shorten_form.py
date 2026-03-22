"""
ShortenForm component — the core interactive unit of the shortener.

Flow:
    1. User types a URL
    2. Clicks "Shorten ➝‬"
    3. Lively calls the handler, creates ShortURL, updates the result live
    4. Copy button lets the user grab the short URL instantly
"""
from duck.shortcuts import resolve

from duck.html.components.container import FlexContainer, Container
from duck.html.components.form import Form
from duck.html.components.input import Input
from duck.html.components.button import RaisedButton, FlatButton
from duck.html.components.label import Label
from duck.html.components.paragraph import Paragraph
from duck.html.components.script import Script
from duck.html.components import to_component


# Clipboard copy with visual feedback
COPY_SCRIPT = """
function copyShortUrl(btnId, urlId) {
    var text = document.getElementById(urlId).innerText;
    navigator.clipboard.writeText(text).then(function() {
        var btn = document.getElementById(btnId);
        var prev = btn.innerText;
        btn.innerText = '✓ Copied';
        btn.style.color = '#00ff87';
        btn.style.borderColor = 'rgba(0,255,135,0.5)';
        btn.style.background = 'rgba(0,255,135,0.08)';
        setTimeout(function() {
            btn.innerText = prev;
            btn.style.color = '';
            btn.style.borderColor = '';
            btn.style.background = '';
        }, 2200);
    });
}
"""


class ResultBox(FlexContainer):
    """
    Shows the shortened URL and a copy button.
    Hidden until a URL is successfully shortened.
    """
    def on_create(self):
        super().on_create()
        self.style.update({
            "flex-direction": "column",
            "gap": "10px",
            "padding": "16px 18px",
            "border-radius": "12px",
            "background": "rgba(0,255,135,0.05)",
            "border": "1px solid rgba(0,255,135,0.2)",
            "margin-top": "16px",
            "display": "none",
        })

        # Prompt line above the URL
        prompt = to_component("", "div", no_closing_tag=False)
        prompt.klass = "result-line"
        prompt.inner_html = "short url ready"

        # Row: URL + copy button
        row = FlexContainer(
            style={
                "flex-direction": "row",
                "align-items": "center",
                "gap": "12px",
                "flex-wrap": "wrap",
            },
        )

        self.url_text = Label(text="")
        self.url_text.id = "short-url-result"
        self.url_text.style.update({
            "font-family": "var(--mono)",
            "font-size": "1rem",
            "font-weight": "500",
            "color": "var(--accent)",
            "word-break": "break-all",
            "flex": "1",
            "letter-spacing": "0.01em",
        })

        self.copy_btn = FlatButton(id="copy-short-url-btn", text="Copy")
        self.copy_btn.style.update({
            "font-size": "0.78rem",
            "font-weight": "600",
            "padding": "6px 16px",
            "border": "1px solid rgba(255,255,255,0.14)",
            "border-radius": "8px",
            "color": "rgba(255,255,255,0.55)",
            "white-space": "nowrap",
            "cursor": "pointer",
            "transition": "all 0.18s",
            "background": "transparent",
            "font-family": "var(--mono)",
        })
        self.copy_btn.props["type"]    = "button"
        self.copy_btn.props["onclick"] = "copyShortUrl('copy-short-url-btn','short-url-result')"

        row.add_children([self.url_text, self.copy_btn])
        self.add_children([prompt, row])

    def show(self, short_url: str):
        self.url_text.text  = short_url
        self.style["display"] = "flex"

    def hide(self):
        self.style["display"] = "none"


class ErrorBox(Container):
    """
    Displays a validation or server error. Hidden until an error occurs.
    """
    def on_create(self):
        super().on_create()
        self.style.update({
            "padding": "12px 16px",
            "border-radius": "10px",
            "background": "rgba(255,77,109,0.07)",
            "border": "1px solid rgba(255,77,109,0.25)",
            "margin-top": "12px",
            "display": "none",
        })

        self.msg = Paragraph()
        self.msg.style.update({
            "color": "#ff6b84",
            "font-size": "0.85rem",
            "font-family": "var(--mono)",
            "margin": "0",
        })
        self.add_child(self.msg)

    def show(self, message: str):
        self.msg.inner_html   = message
        self.style["display"] = "block"

    def hide(self):
        self.style["display"] = "none"


class ShortenForm(Form):
    """
    Complete URL shortening form.

    Accepts an optional `on_shortened` callback that receives the new
    ShortURL instance — useful for refreshing parent components like StatsBar.

    Usage:
        self.form = ShortenForm(on_shortened=self.stats.refresh)
    """
    def on_create(self):
        super().on_create()
        self.style.update({
            "flex-direction": "column",
            "gap": "0",
            "width": "100%",
        })

        self.on_shortened = self.kwargs.get("on_shortened")
        self.stats_bar    = self.kwargs.get("stats_bar")

        # Input row
        input_row = FlexContainer(
            style={
                "flex-direction": "row",
                "gap": "10px",
                "flex-wrap": "wrap",
            },
        )

        self.input = Input(type="url", placeholder="https://your-very-long-url-goes-here.com/…")
        self.input.id = "url-input"
        self.input.props["name"] = "url"
        self.input.style.update({
            "flex": "1",
            "min-width": "200px",
            "padding": "13px 16px",
            "background": "rgba(255,255,255,0.04)",
            "border": "1px solid rgba(255,255,255,0.1)",
            "border-radius": "10px",
            "color": "var(--text)",
            "font-size": "0.9rem",
            "font-family": "var(--mono)",
            "outline": "none",
            "transition": "border-color 0.15s, box-shadow 0.15s",
        })

        self.btn = RaisedButton(text="Shorten ➝‬")
        self.btn.bg_color = "var(--accent)"
        self.btn.color    = "#070809"
        self.btn.props["type"] = "submit"
        self.btn.style.update({
            "padding": "13px 22px",
            "border-radius": "10px",
            "font-size": "0.9rem",
            "font-weight": "700",
            "white-space": "nowrap",
            "cursor": "pointer",
            "letter-spacing": "0.01em",
            "font-family": "var(--sans)",
            "border": "none",
        })

        input_row.add_children([self.input, self.btn])

        # Bind submit
        self.bind(
            "submit",
            self.handle_shorten,
            update_targets=[self.stats_bar],
            update_self=True,
        )

        # Result and error
        self.result = ResultBox()
        self.error  = ErrorBox()

        self.add_children([input_row, self.result, self.error])
        self.add_child(Script(inner_html=COPY_SCRIPT))

    def handle_shorten(self, btn, event, form_inputs, ws):
        """
        Lively event handler — runs server-side on form submit.
        Validates the URL, creates the ShortURL, and updates the UI live.
        """
        from web.backend.django.duckapp.core.models import ShortURL
        from django.core.exceptions import ValidationError
        from django.core.validators import URLValidator

        # Reset previous state
        self.error.hide()
        self.result.hide()

        raw_url = form_inputs.get("url", "").strip()

        if not raw_url:
            self.error.show("Please enter a URL before shortening.")
            return

        # Validate URL format
        validator = URLValidator()
        try:
            validator(raw_url)
        except ValidationError:
            self.error.show(
                "That doesn't look like a valid URL. "
                "Make sure it starts with http:// or https://"
            )
            return

        # Create the short URL
        try:
            short = ShortURL.shorten(raw_url)
        except Exception:
            self.error.show("Something went wrong. Please try again.")
            return

        # Build the full short URL using the configured base domain
        base = resolve("home")
        full_short_url = f"{base}/s/{short.short_code}"

        self.result.show(full_short_url)

        # Notify parent (e.g. StatsBar.refresh) if callback provided
        if callable(self.on_shortened):
            self.on_shortened()
