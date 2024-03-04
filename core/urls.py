from django.urls import path
from .views import *

urlpatterns = [
    path("add-category/", CreateProductCategory.as_view(), name="product-category"),
    path("list-category/", ListProductCategory.as_view(), name="list-category"),
    path(
        "update-category/<int:pk>/",
        UpdateProductCategory.as_view(),
        name="update-category",
    ),
    path(
        "delete-category/<int:pk>/",
        DeleteProductCategory.as_view(),
        name="delete-category",
    ),
]
