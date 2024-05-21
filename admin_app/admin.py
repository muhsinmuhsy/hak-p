from django.contrib import admin
from admin_app.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Size)
admin.site.register(ColorImage)
admin.site.register(Color)