from django.urls import path
from . import views

urlpatterns = [
    path('UserRegistrationview/',views.UserRegistrationview.as_view(),name='Userregister'),
    path('Userloginview/',views.LoginRegisterApi.as_view(),name='login'),
    path('productcreate/',views.ProductCreate.as_view(),name='create'),
    path('ordercustomer/',views.order.as_view(),name='order'),
    path('productupdate/<str:id>',views.productupdate.as_view(),name='update'),
    path('delete/<str:id>',views.deleteorder.as_view(),name='delete')
]