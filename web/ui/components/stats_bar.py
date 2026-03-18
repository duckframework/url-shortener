"""
StatsBar component — shows total links shortened and total clicks site-wide.
Refreshes live after each shorten action via Lively.
"""
from duck.html.components.container import FlexContainer
from duck.html.components.label import Label


class StatCard(FlexContainer):
    """
    A single stat pill — a large number above a small descriptor label.
    """
    def on_create(self):
        super().on_create()
        self.style.update({
            "flex-direction": "column",
            "align-items": "center",
            "gap": "4px",
            "padding": "16px 28px",
            "border-radius": "12px",
            "background": "rgba(255,255,255,0.04)",
            "border": "1px solid rgba(255,255,255,0.08)",
            "min-width": "130px",
        })

        self.value_label = Label(text=str(self.kwargs.get("value", "0")))
        self.value_label.style.update({
            "font-size": "2rem",
            "font-weight": "700",
            "color": "#fff",
            "letter-spacing": "-0.02em",
        })

        self.desc_label = Label(text=self.kwargs.get("label", ""))
        self.desc_label.style.update({
            "font-size": "0.75rem",
            "color": "rgba(255,255,255,0.4)",
            "text-transform": "uppercase",
            "letter-spacing": "0.08em",
        })

        self.add_children([self.value_label, self.desc_label])


class StatsBar(FlexContainer):
    """
    Displays site-wide stats: total links shortened and total clicks.

    Usage:
        self.stats = StatsBar()
        # After a new URL is shortened:
        self.stats.refresh()
    """
    def on_create(self):
        super().on_create()
        self.style.update({
            "flex-direction": "row",
            "gap": "12px",
            "justify-content": "center",
            "flex-wrap": "wrap",
            "margin-top": "8px",
        })

        total_links, total_clicks = self.fetch()
        self.links_card = StatCard(value=total_links, label="Links Shortened")
        self.clicks_card = StatCard(value=total_clicks, label="Total Clicks")
        self.add_children([self.links_card, self.clicks_card])

    def fetch(self):
        from web.backend.django.duckapp.core.models import ShortURL
        from django.db.models import Sum
        
        total_links = ShortURL.objects.count()
        total_clicks = ShortURL.objects.aggregate(total=Sum("click_count"))["total"] or 0
        return total_links, total_clicks

    def refresh(self):
        """
        Pulls fresh stats and updates both cards in place.
        Lively will patch only the changed text nodes — no full re-render.
        """
        total_links, total_clicks = self.fetch()
        self.links_card.value_label.text = str(total_links)
        self.clicks_card.value_label.text = str(total_clicks)
