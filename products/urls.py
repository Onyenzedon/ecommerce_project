from products import views
from django.urls import path

app_name = "products"

urlpatterns = [
    path("products/", views.all_products, name="products"),
    path("create-product/", views.create_product, name="create-product"),
    path("update-product/<slug:slug>/<int:id>/", views.update_product, name="update-product"),
    path("<slug:slug>/", views.all_products, name="product_detail"),
]
