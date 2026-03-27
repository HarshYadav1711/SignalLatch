from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Flag
from .serializers import FlagListQuerySerializer, FlagSerializer, FlagStatusUpdateSerializer
from services.flag_review_service import update_flag_status


class FlagListView(APIView):
    def get(self, request):
        query_serializer = FlagListQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query = query_serializer.validated_data

        queryset = Flag.objects.select_related("keyword", "content_item").all()
        status_value = query.get("status")
        min_score = query.get("min_score")
        keyword_name = query.get("keyword")

        if status_value:
            queryset = queryset.filter(status=status_value)
        if min_score:
            queryset = queryset.filter(score__gte=min_score)
        if keyword_name:
            queryset = queryset.filter(keyword__name__icontains=keyword_name.strip())

        serializer = FlagSerializer(queryset.order_by("-score", "id"), many=True)
        return Response({"count": len(serializer.data), "results": serializer.data})


class FlagReviewUpdateView(APIView):
    def patch(self, request, flag_id):
        try:
            flag = Flag.objects.select_related("content_item").get(id=flag_id)
        except Flag.DoesNotExist:
            return Response(
                {"detail": "Flag not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = FlagStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_flag_status(flag, serializer.validated_data["status"])
        flag.refresh_from_db()

        return Response(
            {"message": "Flag review status updated.", "flag": FlagSerializer(flag).data}
        )
