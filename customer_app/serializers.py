from rest_framework import serializers
from admin_app.models import Category, Product, ProductVariant, Color, ColorImage

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
        
        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        

class ColorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorImage
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    images = ColorImageSerializer(many=True, read_only=True)

    class Meta:
        model = Color
        fields = '__all__'
        

class ProductVariantSerializer(serializers.ModelSerializer):
    size_name = serializers.SerializerMethodField()
    color = ColorSerializer()
    
    class Meta:
        model = ProductVariant
        fields = '__all__'

    def get_size_name(self, obj):
        return obj.size.name if obj.size else None



# class ProductVariantSerializer(serializers.ModelSerializer):
#     size_name = serializers.CharField(source='size.name', read_only=True)
#     color_name = serializers.CharField(source='color.name', read_only=True)

#     class Meta:
#         model = ProductVariant
#         fields = ['id', 'actual_price', 'discount_price', 'stock', 'product', 'size', 'size_name', 'color', 'color_name']


# class ProductSerializer(serializers.ModelSerializer):
#     variants = ProductVariantSerializer(many=True, read_only=True)

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'category', 'variants']