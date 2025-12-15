from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderItem, Product

@receiver(post_save,sender=OrderItem)
def updatedstock(sender, instance, created, **kwargs):
    if not created:
        return
    quantity = instance.quantity
    p = instance.product
    p.stock -= quantity
    p.save()
@receiver(post_delete,sender=OrderItem)
def updatedstock(sender, instance, **kwargs):
        
    quantity = instance.quantity
    p = instance.product
    p.stock += quantity
    p.save()























# @receiver(m2m_changed, sender=Order.items.through)
# def update_stock_and_total(sender, instance, action, **kwargs):
#     if action == "post_add":

#         # Get all order items for this order
#         order_items = OrderItem.objects.filter(order=instance)

#         total_amount = 0

#         for item in order_items:
#             product = item.product
#             qty = item.quantity

#             # Reduce stock
#             if product.stock >= qty:
#                 product.stock -= qty
#                 product.save()
#             else:
#                 print(f"Not enough stock for {product.name}")

#             # Add to total
#             total_amount += (product.price * qty)

#         # Update order total
#         instance.total_amount = total_amount
#         instance.save()