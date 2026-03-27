from rest_framework import serializers

from .models import Flag


class FlagSerializer(serializers.ModelSerializer):
    keyword_name = serializers.CharField(source="keyword.name", read_only=True)
    content_title = serializers.CharField(source="content_item.title", read_only=True)
    content_source = serializers.CharField(source="content_item.source", read_only=True)

    class Meta:
        model = Flag
        fields = (
            "id",
            "keyword",
            "keyword_name",
            "content_item",
            "content_title",
            "content_source",
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


class FlagStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Flag.Status.choices)


class FlagListQuerySerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Flag.Status.choices, required=False)
    min_score = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False, min_value=0
    )
    keyword = serializers.CharField(required=False, allow_blank=False)
