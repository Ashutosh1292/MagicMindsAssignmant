from . views import *
from django.urls import path


urlpatterns=[
    path("add_product",AddProduct.as_view(),name="add_product"),
    path("get_product",GetProduct.as_view(),name="get_product"),
    path("update_product",UpdateProduct.as_view(),name="update_product"),
    path("deleate_product",DeleteProduct.as_view(),name="deleate_product"),
    path("search",SearchProduct.as_view(),name="search"),
    path("add_sales",AddSales.as_view(),name="add_sales"),
    path("get_score",GetProductScore.as_view(),name="get_score"),
    path("get_query",allQueries.as_view(),name="get_query"),
    path("sale_log",GetSellLog.as_view(),name="sale_log")
]
