from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .scan_service import run_scan


class ApiRootView(APIView):
    def get(self, request):
        return Response(
            {
                "message": "SignalLatch backend is running.",
                "endpoints": {
                    "create_keyword": "/keywords/",
                    "scan": "/scan/",
                    "list_flags": "/flags/",
                    "review_flag": "/flags/{id}/",
                },
            },
            status=status.HTTP_200_OK,
        )


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
