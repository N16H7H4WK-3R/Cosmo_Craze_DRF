from userauths.custom_permissions import IsAdminAuthenticated
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import *
from .serializers import *


# Create your views here.


class CreateProductCategory(APIView):
    permission_classes = [IsAuthenticated, IsAdminAuthenticated]

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
