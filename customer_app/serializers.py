from rest_framework import serializers
from admin_app.models import Category

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
        
    