from django.db import models


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
        return (value or "").strip().lower()

    def __str__(self):
        return self.name
