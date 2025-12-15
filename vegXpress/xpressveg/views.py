from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ValidationError
from . import validators, models
from core.exception import SerializerError
from core.utils import *
from core.general import *
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, OrderSerializer
# Create your views here.

class UserRegistrationview(APIView):
  
    def post(self, request):
        try:
            validator = validators.CustomerRegisterValidator(data=request.data)
            if not validator.is_valid():
                raise SerializerError(validator.errors)
            
            validated_data = validator.validated_data
            email = validated_data.get("email")
            mobile = validated_data.get("mobile")

            if models.CustomUser.objects.filter(email=email).exists():
                return Response(
                    error_response(message="Email Already Exists", errors="Email Already Exists"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            if models.CustomUser.objects.filter(mobile=mobile).exists(): #added by kiran
                return Response(
                    error_response(message="mobile Already Exists. Try another Mobile Number", errors="Mobile Already Exists"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            password = validated_data.pop("password")
            user_obj = models.CustomUser.objects.create(
                email=email,
                username= validated_data.get("username"),
                mobile=mobile,
                role=validated_data.get("role"),
            )
            user_obj.set_password(password)
            user_obj.save()
            return Response(
                success_response(
                    message="User registered successfully",
                    data={
                        "id": (user_obj.id),
                        "User_name": user_obj.username,
                        "email": user_obj.email,
                        "mobile": user_obj.mobile,
                        "role": user_obj.role  
                    }
                ),
                status=status.HTTP_201_CREATED
            )
            

        except Exception as e:
            return Response(
                error_response(
                    message='Something went wrong',
                    errors=str(e)
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
 



class LoginRegisterApi(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        try:
            validator = validators.LoginValidators(data = request.data)
            if not validator.is_valid():
                raise SerializerError(validator.errors)
            validate_data = validator.validated_data
            email = validate_data['email']
            pwd = validate_data['password']
            
            try:
                 user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response(
                    error_response(
                        message="No User Found with the given email.",
                        errors="No User Found with the given email."
                    ),
                    status=status.HTTP_404_NOT_FOUND
                )
           
            
            user = authenticate(request, username=email, password=pwd)
             
            if not user:
                return Response(
                    error_response(
                       message="Invalid email or password.",
                        errors={"Password": ["Incorrect Password"]}
                    ),
                    status=status.HTTP_401_UNAUTHORIZED
                )
            tokens = get_tokens_for_user(user)
            
            return Response(
                success_response(
                    message="Login successful",
                    data=tokens
                ),
                status=status.HTTP_200_OK
            )
             
        except Exception as e:
             return Response(
                error_response(
                    message="Something went wrong",
                    errors=str(e)
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductCreate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  


    def get(self, request):
        try:
            obj = models.Product.objects.all()
            serializer = ProductSerializer(obj,many=True,context={"request": request})

            return Response(
                success_response(
                    message="Products fetched successfully",
                    data=serializer.data
                ),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                error_response(
                    message="Something went wrong",
                    errors=str(e)
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  

    def post(self, request):
        try:
            validator = validators.ProductCreateValidator(data=request.data)

            if not validator.is_valid():
                raise SerializerError(validator.errors)

            validated_data = validator.validated_data

            name = validated_data.get("name")
            price = validated_data.get("price")
            stock = validated_data.get("stock")
            product_image = validated_data.get("product_image")
          
            if models.Product.objects.filter(name=name, user=request.user).exists():
                return Response(
                    error_response(
                        message="Product already exists",
                        errors={"name": ["Product with this name already exists for this user"]}
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                p = models.CustomUser.objects.get(id = request.user.id )

            except:
                 return Response(
                    error_response(
                        message="Product already exists",
                        errors={"name": ["Product with this name already exists for this user"]}
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )

            product = models.Product.objects.create(
                user=p,
                name=name,
                price=price,
                stock=stock,
                product_image=product_image
            )
            product.save()
           
            return Response(
                success_response(
                    message="Product created successfully",
                    data={
                        "id": product.id,
                        "name": product.name,
                        "price": (product.price),
                        "stock": product.stock,
                        "product_image": request.build_absolute_uri(product.product_image.url) if product.product_image else None

                    }
                ),
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response(
                error_response(
                    message="Something went wrong",
                    errors=str(e)
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class order(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self, request):
        try:
            obj = models.Order.objects.all()
            serializer = OrderSerializer(obj,many=True)
            

            return Response(
                success_response(
                    message="orders fetched successfully",
                    data=serializer.data
                ),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                error_response(
                    message="Something went wrong",
                    errors=str(e)
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  
    def post(self, request):
        validator = validators.OrderValidators(data=request.data)

        if not validator.is_valid():
             return Response(
                error_response(message="Invalid Data", errors=validator.errors),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        customer = CustomUser.objects.get(id=validator.validated_data['customer'])
        seller = CustomUser.objects.get(id=validator.validated_data['buyer'])
        products_data = validator.validated_data['items']

        order = models.Order.objects.create(customer=customer, seller=seller)

        total_price = 0

        for p in products_data:
            product = models.Product.objects.get(id=p['item'])
            qty = int(p['quantity'])

            models.OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                total_amount=product.price*qty
            )

            total_price += product.price * qty

        order.total_amount = total_price
        order.save()

        return Response(
            success_response(
                data={
                    "order_id": str(order.id),
                    "customer": str(customer.username),
                    "seller": str(seller.username),
                    "products": products_data,
                    "total_price": total_price
                },
                message="Order created successfully"
            ),
            status=status.HTTP_201_CREATED
        )
class productupdate(APIView):
    def put(self,request,id):
        obj = models.Product.objects.get(id=id)
        validator = validators.ProductCreateValidator(data=request.data)
        if validator.is_valid():
            validator_data = validator.validated_data
            for key,value in validator_data.items():
                setattr(obj,key,value)
            obj.save()
            
            return Response(
                success_response(
                    message="Products updated successfully",
                    data=validator_data
                ),
                status=status.HTTP_200_OK
            )
        raise SerializerError(validator.errors)
    def patch(self,request,id):
        obj = models.Product.objects.get(id=id)
        validator = validators.ProductCreateValidator(data=request.data,partial=True)
        if validator.is_valid():
            validator_data = validator.validated_data
            obj.stock+=validator_data['stock']
            obj.save()

            return Response(
                success_response(
                    message="stock updated successfully",
                    data=validator_data
                ),
                status=status.HTTP_200_OK
            )
        raise SerializerError(validator.error)
    
class deleteorder(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,id):
        try:
            obj = models.Order.objects.get(id=id)
        except models.Order.DoesNotExist:
            return Response(error_response(message="orderobjectnotfound",error="invalid_id"))
        if request.user == obj.customer:
            orderitem = models.OrderItem.objects.filter(order=id)
            orderitem.delete()
            obj.delete()
            return Response(
                success_response(
                    message="order deleted successfully",
                    data="orderdeleted"
                ),
                status=status.HTTP_200_OK
            )
        return Response(error_response(message="invalid user",errors="authentication error")) 
