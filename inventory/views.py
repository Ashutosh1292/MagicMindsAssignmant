from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView , UpdateAPIView
from rest_framework.response import Response
from . models import Products , SaleLog
from .serialzar import ProductSerializer , SalelogSerializer
from rest_framework import status
from django.db.models import Q , Count , Sum
import json
import logging

logger = logging.getLogger(__name__)

class AddProduct(GenericAPIView):
    serializer_class = ProductSerializer
    def post(self,request):
        try:
            name= request.data.get("name")
            description = request.data.get("description")
            price=request.data.get("price")
            category = request.data.get("category")
            inventory_count=request.data.get("inventory_count")
            procucts = Products(name=name,description=description,price=price,category=category,inventory_count=inventory_count)
            # print(procucts.query)
            procucts.save()
            return Response({"status":200,"message":"Product saved"})
        except Exception as e:
            logger.error(f"Error occurred in my_view: {str(e)}", exc_info=True)
            return HttpResponse("An error occurred", status=500)
        
class GetProduct(GenericAPIView):
    serializer_class = ProductSerializer
    def get(self,request):
        try:
            products = Products.objects.all()
            # print(products.query)
            products_list = list(products.values("id","name","description","price","category","inventory_count"))
            response={}
            response["products"] = products_list
            response["status"] = 200
            print(response)
            return JsonResponse(response,safe=False)
        except Exception as e:
            return JsonResponse({"status":400,"message":str(e)})
        

class UpdateProduct(GenericAPIView):
    serializer_class = ProductSerializer
    def post(self, request, *args, **kwargs):
        try:
            product_id = request.data.get('id') 
            product = Products.objects.get(id=product_id)
            print(product.query)
            product.name = request.data.get("name", product.name)
            product.description = request.data.get("description", product.description)
            product.price = request.data.get("price", product.price)
            product.category = request.data.get("category", product.category)
            product.inventory_count = request.data.get("inventory_count", product.inventory_count)

            product.save() 

            return Response({
                "status": 200,
                "message": "Product updated successfully",
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "category": product.category,
                    "inventory_count": product.inventory_count
                }
            }, status=status.HTTP_200_OK)

        except Products.DoesNotExist:
            return Response({"status": 404, "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({"status": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteProduct(GenericAPIView):
    serializer_class = ProductSerializer
    def post(self, request):
        try:
            product_id = request.data.get("id") 
            product = Products.objects.get(id=product_id)
            print(product.query)
            product.delete()

            return Response({"status": 200, "message": "Product deleted successfully"}, status=status.HTTP_200_OK)

        except Products.DoesNotExist:
            return Response({"status": 404, "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SearchProduct(GenericAPIView):
    serializer_class = ProductSerializer
    def post(self, request):
        try:
            keyword = request.data.get('query', '').strip()
            if not keyword:
                return Response({"status": 400, "message": "Please provide a search keyword"}, status=status.HTTP_400_BAD_REQUEST)
            products = Products.objects.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword) |  Q(category__icontains=keyword)
            )
            print(products.query)
            products_list = list(products.values("id", "name", "description", "price", "category", "inventory_count"))
            response = {
                "status": 200,
                "products": products_list
            }

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AddSales(GenericAPIView):
    serializer_class = SalelogSerializer
    def post(self, request):
        try:
            quantity = request.data.get('sale_quantity')
            product_id = request.data.get('product_id')
            product = Products.objects.get(id=product_id)
            # print(product.query)
            if quantity > product.inventory_count:
                return Response(
                    {"status": 400, "message": "Insufficient stock for the sale"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            print(product)
            sale_log = SaleLog.objects.create(product_id=product, sale_quantity=quantity)
            print(sale_log)
            product.inventory_count -= quantity
            product.save()
            return Response({"status":200,"message":f"{quantity} iteams sold"})
            

        except Exception as e:
            return Response({"status": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetProductScore(GenericAPIView):
    serializer_class = ProductSerializer
    def get(self,request):
        try:
            # products = Products.objects.annotate(sale_count=Count('salelog')) 
            products = Products.objects.annotate(total_sale_quantity=Sum('salelog__sale_quantity')).order_by('-total_sale_quantity') 
            print(products.query)
            products_list = []
            for product in products:
                popularity_score = product.total_sale_quantity * 0.1 if product.total_sale_quantity else 0
                products_list.append({
                    'id': product.id,
                    'name': product.name,
                    'total_sale_quantity': product.total_sale_quantity or 0 ,
                    "popularity_score":popularity_score
                })
            
            response = {
                "status": 200,
                "products": products_list
            }

            return JsonResponse(response, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"status": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class allQueries(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        try:
            # query = request.data.get("query") 
            from django.db.models import Subquery, OuterRef, Avg
            # import js

            # from pyspark.sql import SparkSession
            # spark = SparkSession.builder.appName("DataFrameExample").getOrCreate()
            # data = {[1,2,3,4],[3,4,5],[4,5,6]}
            # df = spark.createDataFrame(data)
            
            # Show DataFrame structure and contents
            # df.show()

            # Print DataFrame schema
            # df.printSchema()
            # products_gt=SaleLog.objects.aggregate(id_avg=Avg('id'))["id"]
            # print(products_gt)
            # products = Products.objects.filter(price__gt=Subquery(products_gt))
            # print(products)
            from django.core.serializers import serialize
            products = Products.objects.filter(id_is = 2)
            data = list(products.values())
            print(data)
            result = {
                "sql":str(products.query),
                "orm": data
            }
            print(result)
            return JsonResponse(result, status=status.HTTP_200_OK)  # Correcting the return here

        except Exception as e:
            # Catch the exception and return a meaningful response
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetSellLog(APIView):
    def get(self,request):
        # log = SaleLog.objects.select_related("product_id").all()
        # log = SaleLog.objects.all()
        log = SaleLog.objects.values("product_id")
        # log = SaleLog.objects.only("product_id")
        
        log=list(log.values())
        print(log)

        return JsonResponse(log, status=status.HTTP_200_OK,safe=False)

