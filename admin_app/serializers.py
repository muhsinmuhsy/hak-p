from rest_framework import serializers
from admin_app.models import *

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    class Meta:
        model = Category
        fields = '__all__'
        
       

        
        
# class ProductSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()

#     def get_image(self, obj):
#         request = self.context.get('request')
#         if obj.image:
#             return request.build_absolute_uri(obj.image.url)
#         return None
    
#     class Meta:
#         model = Product
#         fields = '__all__'
                                                                  
                                                                  
                                                                  


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

# class ColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Color
#         fields = '__all__'


 

class ColorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorImage
        fields = ('id', 'image', 'name')


class ColorSerializer(serializers.ModelSerializer):
    images = ColorImageSerializer(many=True, read_only=True)

    class Meta:
        model = Color
        fields = ('id', 'product', 'name', 'images')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductVariantListSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    color = ColorSerializer()

    class Meta:
        model = ProductVariant
        fields = '__all__'
        
        
        
class ProductVariantAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        
        


    # def create(self, validated_data):
    #     size_data = validated_data.pop('size')
    #     color_data = validated_data.pop('color')

    #     size, _ = Size.objects.get_or_create(**size_data)
    #     color, _ = Color.objects.get_or_create(**color_data)

    #     variant = ProductVariant.objects.create(size=size, color=color, **validated_data)
    #     return variant
