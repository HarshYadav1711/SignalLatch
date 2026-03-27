from rest_framework import serializers

from .models import Keyword


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ("id", "name")

    def validate_name(self, value):
        normalized = Keyword.normalize_name(value)
        if not normalized:
            raise serializers.ValidationError("Keyword name cannot be empty.")
        return normalized
