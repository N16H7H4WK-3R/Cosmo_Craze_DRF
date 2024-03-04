from django.urls import path
from .views import *

urlpatterns = [
    path("category/", CreateProductCategory.as_view(), name="product-category"),
]
