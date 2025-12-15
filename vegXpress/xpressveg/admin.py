from django.contrib import admin
from .models import CustomUser,Product,OrderItem,Order


admin.site.register(CustomUser) 
admin.site.register(Product) 
admin.site.register(OrderItem)
admin.site.register(Order)  