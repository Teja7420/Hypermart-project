from rest_framework import serializers
from .models import CustomUser, Product, Order,OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "mobile"]
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "user","product_image"]

    def get_product_image_url(self, obj):
        request = self.context.get('request')
        if obj.product_image:
            return request.build_absolute_uri(obj.product_image.url)
        return None

class ProductSerializerForOrder(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "price"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializerForOrder(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "total_amount"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "seller", "customer","total_amount","items",]


