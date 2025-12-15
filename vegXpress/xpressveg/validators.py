from rest_framework import serializers
from .models import CustomUser, UserRoles
import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
 


def email_validator(value):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        raise ValidationError("Enter a valid Email Format.")
     

def validate_password(password):
    if len(password) < 5:
        raise ValidationError(
            ('Password must be at least 5 characters long.'),
            code='password_length'
        )
   

def mobile_validate(mobile):
    # Create the validator
    mobile_number_validator = RegexValidator(
        regex=r'^[6-9]\d{9}$',
        message="Mobile number must be in correct format."
    )
    


class CustomerRegisterValidator(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=30, allow_blank=False, error_messages={
        'required': 'Full Name is required.',
        'blank': 'Full Name cannot be blank.'
    })
    email = serializers.EmailField(required=True, allow_blank=False, error_messages={
        'required': 'Email is required.',
        'blank': 'Email cannot be blank.'
    }, validators=[email_validator])
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=8, error_messages={
        "required": "Password is a required field.",
        "null": "Password field cannot be null.",
        "blank": "Password field cannot be empty."
    }, validators=[validate_password])
    
    mobile = serializers.CharField(max_length=10, required = True, allow_null=True, allow_blank=True, error_messages={
        'required':'Mobile is required',
        'null':'Mobile cannot be null',
        'blank':'Mobile cannot be blank'
    }, validators=[mobile_validate])
    role= serializers.ChoiceField(choices=UserRoles.choices, required=False,default = UserRoles.CUSTOMER,error_messages={
            'required': 'User role is required.',
            'invalid_choice': 'Invalid user role. Choose from  ADMIN, CUSTOMER.'
        }
    )
class LoginValidators(serializers.Serializer):


    
    email = serializers.CharField(required = True, allow_blank = False,allow_null= False,error_messages = {
        'NULL':'email name could not allow null value',
        'Blank': 'email name could not allow blank',
        'required':'email name required'},validators=[email_validator])
    

    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=8, error_messages={
        "required": "Password is a required field.",
        "null": "Password field cannot be null.",
        "blank": "Password field cannot be empty."
    })
 

class ProductCreateValidator(serializers.Serializer):
    name = serializers.CharField(required = True)
    price = serializers.DecimalField(max_digits=10,decimal_places=2,required = False)
    stock = serializers.IntegerField(required = False)
    product_image = serializers.ImageField(required = False)

    

class orderitemsvalidators(serializers.Serializer):
    item = serializers.CharField(required= True)
    quantity = serializers.DecimalField(max_digits=10,decimal_places=2, default=1.0)


class OrderValidators(serializers.Serializer):
    buyer = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=8, error_messages={
        "required": "buyer is a required field.",
        "null": "buyer field cannot be null.",
        "blank": " buyer field cannot be empty."
    })
    customer = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=8, error_messages={
        "required": "customer is a required field.",
        "null": "customer field cannot be null.",
        "blank": "customer field cannot be empty."
    })
    items = serializers.ListField(child=orderitemsvalidators(),required=True,error_messages = {
        'required':'items field is required'
    })
  