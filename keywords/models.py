from django.db import models
from django.utils.text import slugify


class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def clean(self):
        super().clean()
        self.name = self.normalize_name(self.name)

    def save(self, *args, **kwargs):
        self.name = self.normalize_name(self.name)
        return super().save(*args, **kwargs)

    @staticmethod
    def normalize_name(value: str) -> str:
        normalized = slugify((value or "").strip()).replace("-", " ")
        return " ".join(normalized.split())

    def __str__(self):
        return self.name
