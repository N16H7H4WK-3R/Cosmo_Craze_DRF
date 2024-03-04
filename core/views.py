from rest_framework import generics
from rest_framework.permissions import AllowAny
from userauths.custom_permissions import IsAdminAuthenticated
from .models import Category
from .serializers import ProductCategorySerializer


class CreateProductCategory(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminAuthenticated]


class ListProductCategory(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]


class UpdateProductCategory(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminAuthenticated]


class DeleteProductCategory(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminAuthenticated]
