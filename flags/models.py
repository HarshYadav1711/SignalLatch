from django.db import models


class Flag(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RELEVANT = "relevant", "Relevant"
        IRRELEVANT = "irrelevant", "Irrelevant"

    keyword = models.ForeignKey("keywords.Keyword", on_delete=models.CASCADE)
    content_item = models.ForeignKey("content.ContentItem", on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_content_last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["keyword", "content_item"],
                name="unique_flag_keyword_content_item",
            )
        ]

    def __str__(self):
        return f"{self.keyword} -> {self.content_item} ({self.status})"
