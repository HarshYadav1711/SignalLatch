from rest_framework import serializers

from .models import Flag


class FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = (
            "id",
            "keyword",
            "content_item",
            "score",
            "status",
            "reviewed_at",
            "reviewed_content_last_updated",
        )

    def validate_score(self, value):
        if value < 0:
            raise serializers.ValidationError("Score must be non-negative.")
        return value

    def validate(self, attrs):
        status = attrs.get("status", getattr(self.instance, "status", Flag.Status.PENDING))
        reviewed_at = attrs.get("reviewed_at", getattr(self.instance, "reviewed_at", None))
        reviewed_last_updated = attrs.get(
            "reviewed_content_last_updated",
            getattr(self.instance, "reviewed_content_last_updated", None),
        )

        if status == Flag.Status.PENDING and (reviewed_at or reviewed_last_updated):
            raise serializers.ValidationError(
                "Pending flags cannot include review timestamps."
            )

        if status == Flag.Status.IRRELEVANT and not reviewed_last_updated:
            raise serializers.ValidationError(
                "Irrelevant flags must store reviewed_content_last_updated."
            )

        return attrs
