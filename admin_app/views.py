from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category, Product
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
# Create your views here.


#------------------------------------- Category ------------------------------------------------------#

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



#------------------------------------- Product ------------------------------------------------------#



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
    

class ProductViewAPIView(APIView):
    def get(self, request, format=None, product_id=None):
        product = Product.objects.get(id=product_id)
        products_and_variants_data = []

        
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



# class ProductAddAPIView(APIView):
#     def post(self, request, format=None):
#         product_data = request.data
#         variants_data = product_data.pop('variants', [])

#         product_serializer = ProductSerializer(data=product_data)
        
#         if product_serializer.is_valid():
#             product = product_serializer.save()

#             for variant_data in variants_data:
#                 variant_data['product'] = product.id
#                 variant_serializer = ProductVariantAddSerializer(data=variant_data)
                
#                 if variant_serializer.is_valid():
#                     variant_serializer.save()
#                 else:
#                     product.delete()  # Rollback
#                     return Response(variant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#             return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
class ProductAddAPIView(APIView):
    @transaction.atomic
    def post(self, request, format=None):
        product_data = request.data
        variants_data = product_data.pop('variants', [])

        product_serializer = ProductSerializer(data=product_data)
        
        if product_serializer.is_valid():
            product = product_serializer.save()

            for variant_data in variants_data:
                variant_data['product'] = product.id
                variant_serializer = ProductVariantAddSerializer(data=variant_data)
                
                if variant_serializer.is_valid():
                    variant_serializer.save()
                else:
                    transaction.set_rollback(True)
                    return Response(variant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
{
    "category": 1,
    "name": "Example Product",
    "description": "This is an example product description.",
    "variants": [
        {
            "size": 1,
            "color": 1,
            "actual_price": "100.00",
            "discount_price": "80.00",
            "stock": 50
        },
        {
            "size": 2,
            "color": 1,
            "actual_price": "100.00",
            "discount_price": "80.00",
            "stock": 30
        }
    ]
}
        
    
    
#------------------------------------- Color ------------------------------------------------------#

class ColorAPIView(APIView):
    def get(self, request):
        colors = Color.objects.all()
        serializer = ColorSerializer(colors, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            product_id = request.data.get('product')
            name = request.data.get('name')
            images_data = request.data.get('images', [])

            color = Color.objects.create(product_id=product_id, name=name)

            for image_data in images_data:
                # Serialize each image data
                image_serializer = ColorImageSerializer(data=image_data)
                if image_serializer.is_valid():
                    # Save the image instance
                    color_image = image_serializer.save()
                    # Associate the created ColorImage with the Color instance
                    color.images.add(color_image)
                else:
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer = ColorSerializer(color)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        

{
    "product": 1,
    "name": "red",
    "images": [
        {
            "name": "c1"
        },
        {  
            "name": "c2"
        },
        {
            "name": "c3"
        }
    ]
}