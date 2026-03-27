from rest_framework.response import Response
from rest_framework.views import APIView


class KeywordsHealthView(APIView):
    def get(self, request):
        return Response({'module': 'keywords', 'status': 'ok'})
