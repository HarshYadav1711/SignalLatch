from rest_framework import serializers

from .models import ContentItem


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ("id", "title", "source", "body", "last_updated")

    def validate_title(self, value):
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_source(self, value):
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("Source cannot be empty.")
        return value

    def validate_body(self, value):
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("Body cannot be empty.")
        return value
