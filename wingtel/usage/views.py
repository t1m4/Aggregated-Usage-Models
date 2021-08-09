# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from wingtel.usage.fill_models import fill_models


class FillModel(APIView):
    def get(self, request, *args, **kwargs):
        fill_models()
        return Response('ok')