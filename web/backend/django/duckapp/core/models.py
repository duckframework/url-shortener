"""
ShortURL model — stores original URLs, short codes, and click counts.
"""
import random
import string

from django.db import models


def generate_short_code(length: int = 6) -> str:
    """
    Generates a random alphanumeric short code, retrying until unique.
    """
    chars = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choices(chars, k=length))
        if not ShortURL.objects.filter(short_code=code).exists():
            return code


class ShortURL(models.Model):
    """
    Represents a shortened URL entry.
    """
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=16, unique=True, db_index=True)
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.short_code} → {self.original_url}"

    @classmethod
    def shorten(cls, original_url: str) -> "ShortURL":
        """
        Creates and saves a new ShortURL with a unique short code.
        """
        return cls.objects.create(
            original_url=original_url,
            short_code=generate_short_code(),
        )

    def increment_clicks(self):
        """
        Atomically increments the click counter and refreshes the instance.
        """
        ShortURL.objects.filter(pk=self.pk).update(
            click_count=models.F("click_count") + 1
        )
        self.refresh_from_db()
