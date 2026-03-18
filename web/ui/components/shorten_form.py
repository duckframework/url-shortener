"""
ShortenForm component — the core interactive unit of the shortener.

Flow:
    1. User types a URL
    2. Clicks "Shorten"
    3. Lively calls the handler creates ShortURL → updates result live
    4. Copy button lets user grab the short URL instantly
"""
from duck.shortcuts import resolve

from duck.html.components.container import FlexContainer, Container
from duck.html.components.form import Form
from duck.html.components.input import Input
from duck.html.components.button import RaisedButton, FlatButton
from duck.html.components.label import Label
from duck.html.components.paragraph import Paragraph
from duck.html.components.script import Script


# Copies the short URL to clipboard and briefly changes the button label
COPY_SCRIPT = """
function copyShortUrl(btnId, urlId) {
    var text = document.getElementById(urlId).innerText;
    navigator.clipboard.writeText(text).then(function() {
        var btn = document.getElementById(btnId);
        var prev = btn.innerText;
        btn.innerText = 'Copied!';
        btn.style.color = '#4ade80';
        btn.style.borderColor = '#4ade80';
        setTimeout(function() {
            btn.innerText = prev;
            btn.style.color = '#ccc';
            btn.style.borderColor = '';
        }, 2000);
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
            "padding": "18px 20px",
            "border-radius": "12px",
            "background": "rgba(255,255,255,0.04)",
            "border": "1px solid rgba(74,222,128,0.25)",
            "margin-top": "16px",
            "display": "none",
        })

        self.eyebrow = Label(text="Your shortened URL")
        self.eyebrow.style.update({
            "font-size": "0.72rem",
            "color": "rgba(255,255,255,0.4)",
            "text-transform": "uppercase",
            "letter-spacing": "0.08em",
        })

        self.row = FlexContainer()
        self.row.style.update({
            "flex-direction": "row",
            "align-items": "center",
            "gap": "10px",
            "flex-wrap": "wrap",
        })

        self.url_text = Label(text="")
        self.url_text.id = "short-url-result"
        self.url_text.style.update({
            "font-size": "1.05rem",
            "font-weight": "600",
            "color": "#4ade80",
            "word-break": "break-all",
            "flex": "1",
        })

        self.copy_btn = FlatButton(id="copy-short-url-btn", text="Copy")
        self.copy_btn.style.update({
            "font-size": "0.78rem",
            "padding": "5px 14px",
            "border": "1px solid rgba(255,255,255,0.18)",
            "border-radius": "8px",
            "color": "rgba(255,255,255,0.6)",
            "white-space": "nowrap",
            "cursor": "pointer",
        })
        self.copy_btn.props["type"] = "button"
        self.copy_btn.props["onclick"] = (
            "copyShortUrl('copy-short-url-btn', 'short-url-result')"
        )

        self.row.add_children([self.url_text, self.copy_btn])
        self.add_children([self.eyebrow, self.row])

    def show(self, short_url: str):
        self.url_text.text = short_url
        self.style["display"] = "flex"

    def hide(self):
        self.style["display"] = "none"


class ErrorBox(Container):
    """
    Displays a validation or server error.
    Hidden until an error occurs.
    """
    def on_create(self):
        super().on_create()
        self.style.update({
            "padding": "12px 16px",
            "border-radius": "10px",
            "background": "rgba(239,68,68,0.1)",
            "border": "1px solid rgba(239,68,68,0.3)",
            "margin-top": "12px",
            "display": "none",
        })

        self._msg = Paragraph()
        self._msg.style.update({
            "color": "#f87171",
            "font-size": "0.88rem",
            "margin": "0",
        })
        self.add_child(self._msg)

    def show(self, message: str):
        self._msg.inner_html = message
        self.style["display"] = "block"

    def hide(self):
        self.style["display"] = "none"


class ShortenForm(Form):
    """
    Complete URL shortening form.

    Accepts an optional `on_shortened` callback that receives the new
    ShortURL instance — useful for refreshing parent components like StatsBar.
    
    Notes:
    - Use the form to collect input from the user. By default, binding to `submit` event to a form automatically prevents 
       default page reload and retrieves all input fields. 
        
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
        self.stats_bar = self.kwargs.get("stats_bar")
        
        # --- Input row ---
        self.input_row = FlexContainer()
        self.input_row.style.update({
            "flex-direction": "row",
            "gap": "10px",
            "flex-wrap": "wrap",
        })

        self.input = Input(
            type="url",
            placeholder="Paste a long URL here…",
        )
        self.input.id = "url-input"
        self.input.props["name"] = "url"
        self.input.style.update({
            "flex": "1",
            "min-width": "220px",
            "padding": "14px 16px",
            "background": "rgba(255,255,255,0.06)",
            "border": "1px solid rgba(255,255,255,0.12)",
            "border-radius": "10px",
            "color": "#ccc",
            "font-size": "0.95rem",
            "outline": "none",
        })

        self.btn = RaisedButton(text="Shorten")
        self.btn.bg_color = "#6366f1"
        self.btn.color = "#fff"
        self.btn.props["type"] = "submit"
        self.btn.style.update({
            "padding": "14px 24px",
            "border-radius": "10px",
            "font-size": "0.95rem",
            "font-weight": "600",
            "white-space": "nowrap",
            "cursor": "pointer",
        })
        
        self.input_row.add_children([self.input, self.btn])
        
        # Bind submit event.
        self.bind(
            "submit",
            self.handle_shorten,
            update_targets=[self.stats_bar],
            update_self=True, # Update the form itself or its descendants
        )
        
        # --- Result and error areas ---
        self.result = ResultBox()
        self.error = ErrorBox()

        self.add_children([self.input_row, self.result, self.error])

        # Copy script — injected once into the page body
        self.copy_script = Script(inner_html=COPY_SCRIPT)
        self.add_child(self.copy_script)

    def handle_shorten(self, btn, event, form_inputs, ws):
        """
        Lively event handler — runs server-side on button click.
        Validates the URL, creates the ShortURL, and updates the UI live.
        """
        from web.backend.django.duckapp.core.models import ShortURL
        from django.core.exceptions import ValidationError
        from django.core.validators import URLValidator

        # Reset previous state
        self.error.hide()
        self.result.hide()
        
        raw_url = form_inputs.get("url", "").strip()

        # Client sends the input value as `value` — but for text inputs
        # we read it from the input's last known value via ws context.
        # Fall back to reading it from the DOM value if empty.
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

        # Show result
        self.result.show(full_short_url)

        # Notify parent (e.g. StatsBar.refresh) if callback provided
        if callable(self.on_shortened):
            self.on_shortened()
