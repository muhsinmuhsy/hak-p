from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from admin_app.models import Category
from customer_app.serializers import CategorySerializer
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