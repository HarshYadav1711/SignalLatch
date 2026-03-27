from django.db import models


class ContentItem(models.Model):
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    body = models.TextField()
    last_updated = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "title"],
                name="unique_contentitem_source_title",
            )
        ]

    def __str__(self):
        return f"{self.source}: {self.title}"
