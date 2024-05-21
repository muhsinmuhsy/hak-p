from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from admin_app.models import Category, Product, ProductVariant
from customer_app.serializers import CategorySerializer, ProductSerializer, ProductVariantSerializer
from rest_framework import status
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes



@permission_classes([IsAuthenticated])
class CategoryListView(APIView):
    def get(self, request, format=None):
        try:
            categories = Category.objects.all()
            if not categories:
                return Response({"message": "No categories found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = CategorySerializer(categories, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
 
class CategoryWithProducts(APIView):
    def get(self, request, format=None, category_id=None):        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        category_serializer = CategorySerializer(category, context={'request': request})
        products = Product.objects.filter(category=category)
        product_serializer = ProductSerializer(products, many=True, context={'request': request})
        
        category_data = category_serializer.data
        category_data['products'] = product_serializer.data

        for product_data in category_data['products']:
            product_id = product_data['id']
            variants = ProductVariant.objects.filter(product_id=product_id)
            variants_serializer = ProductVariantSerializer(variants, many=True, context={'request': request})
            product_data['variants'] = variants_serializer.data
        
        response_data = {
            'category': category_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
# class CategoryWithProducts(APIView):
#     def get(self, request, category_id=None, format=None):        
#         try:
#             category = Category.objects.get(id=category_id)
#         except Category.DoesNotExist:
#             return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(category=category)  # Assuming there's a ForeignKey from Product to Category
#         category_serializer = CategorySerializer(category)
#         product_serializer = ProductSerializer(products, many=True)
        
#         category_data = category_serializer.data
#         category_data['products'] = product_serializer.data
        
#         response_data = {
#             'category': category_data
#         }
        
#         return Response(response_data, status=status.HTTP_200_OK)
        
            
        
        
        
@permission_classes([IsAuthenticated]) 
class ProductWithVariants(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        products_data = []
        for product in products:
            product_serializer = ProductSerializer(product)
            variants = ProductVariant.objects.filter(product=product)
            variants_serializer = ProductVariantSerializer(variants, many=True)
            product_data = product_serializer.data
            product_data['variants'] = variants_serializer.data
            products_data.append(product_data)
        
        response_data = {
            'products': products_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)



    

                
                
                
