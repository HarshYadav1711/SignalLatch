from rest_framework.response import Response
from rest_framework.views import APIView


class FlagsHealthView(APIView):
    def get(self, request):
        return Response({'module': 'flags', 'status': 'ok'})
