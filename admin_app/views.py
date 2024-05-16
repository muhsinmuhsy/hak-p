from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category, Product
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class CategoryListCeateView(APIView):
    def get(self, request, format=None):
        try:
            categories = Category.objects.all()
            if not categories:
                return Response({"message": "No category found"}, status=status.HTTP_204_NO_CONTENT)
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to retrieve Category {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, format=None):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Failed to create category: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class ProductListCeateView(APIView):
#     def get(self, request, format=None):
#         try:
#             products = Product.objects.all()
#             if not products:
#                 return Response({"message": "No product found"}, status=status.HTTP_204_NO_CONTENT)
#             serializer = ProductSerializer(products, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": f"Failed to retrieve product {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#     def post(self, request, format=None):
#         try:
#             serializer = ProductSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": f"Failed to create product: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class ProductListCreateAPIView(APIView):
    
#     def get(self, request, format=None):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         product_data = request.data.get('product', {})
#         variants_data = request.data.get('variants', [])

#         # Serialize product data
#         product_serializer = ProductSerializer(data=product_data)
#         if product_serializer.is_valid():
#             # Save product
#             product = product_serializer.save()

#             # Save product variants
#             for variant_data in variants_data:
#                 variant_data['product'] = product.id
#                 variant_serializer = ProductVariantSerializer(data=variant_data)
#                 if variant_serializer.is_valid():
#                     variant_serializer.save()
#                 else:
#                     # If variant data is invalid, delete the created product and return error
#                     product.delete()
#                     return Response(variant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#             return Response(product_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductListAPIView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        products_and_variants_data = []

        for product in products:
            product_serializer = ProductSerializer(product)
            variants = ProductVariant.objects.filter(product=product)
            variants_serializer = ProductVariantListSerializer(variants, many=True)
            product_data = product_serializer.data
            product_data['variants'] = variants_serializer.data
            products_and_variants_data.append(product_data)
            
        response_data = {
            'products' : products_and_variants_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)



class ProductAddAPIView(APIView):
    def post(self, request, format=None):
        pass
    
    
        
    
    
    
{
    "name": "Product1",
    "description": "werfds",
    "category": 1,
    "variants": [
        {
            "size": {"name": "Medium"},  
            "color": {"name": "Red"},    
            "actual_price": "0.07",
            "discount_price": "12.00",
            "stock": 4,
            "product": 2
        },
        {
            "size": {"name": "Large"},   
            "color": {"name": "Red"},    
            "actual_price": "11.00",
            "discount_price": "11.00",
            "stock": 0,
            "product": 2
        }
    ]
}
