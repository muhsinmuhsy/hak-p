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



class ProductListCreateAPIView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        products_data = []

        for product in products:
            product_data = ProductSerializer(product).data
            variants_data = ProductVariantSerializer(product.productvariant_set.all(), many=True).data
            product_data['variants'] = variants_data
            products_data.append(product_data)

        return Response(products_data)
    
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            
            variants_data = request.data.get('variants', [])
            for variant_data in variants_data:
                variant_data['product'] = product.id
                variant_serializer = ProductVariantSerializer(data=variant_data)
                if variant_serializer.is_valid():
                    variant_serializer.save()
                else:
                    product.delete()
                    return Response(variant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# {
#     "name": "Product1",
#     "description": "werfds",
#     "category": 1,
#     "variants": [
#         {
#             "size": {"name": "Medium"},  // Adjusted to a dictionary
#             "color": {"name": "Red"},    // Adjusted to a dictionary
#             "actual_price": "0.07",
#             "discount_price": "12.00",
#             "stock": 4,
#             "product": 2
#         },
#         {
#             "size": {"name": "Large"},   // Adjusted to a dictionary
#             "color": {"name": "Red"},    // Adjusted to a dictionary
#             "actual_price": "11.00",
#             "discount_price": "11.00",
#             "stock": 0,
#             "product": 2
#         }
#     ]
# }
