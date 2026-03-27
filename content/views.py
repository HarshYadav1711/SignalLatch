from rest_framework.response import Response
from rest_framework.views import APIView


class ContentHealthView(APIView):
    def get(self, request):
        return Response({'module': 'content', 'status': 'ok'})
