from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .scan_service import run_scan


class ScanTriggerView(APIView):
    def post(self, request):
        result = run_scan()
        return Response(
            {
                "message": "Scan completed.",
                "scan": {
                    "created": result.created,
                    "updated": result.updated,
                    "suppressed": result.suppressed,
                    "scanned_pairs": result.scanned_pairs,
                },
            },
            status=status.HTTP_200_OK,
        )
