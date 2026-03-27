from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import KeywordSerializer


class KeywordCreateView(APIView):
    def post(self, request):
        serializer = KeywordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        keyword = serializer.save()
        return Response(
            {"message": "Keyword created.", "keyword": KeywordSerializer(keyword).data},
            status=status.HTTP_201_CREATED,
        )
