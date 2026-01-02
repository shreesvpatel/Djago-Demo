from rest_framework import serializers
from .models import *
# from django.contrib.auth import authenticate
# from django.contrib.auth.hashers import check_password
# from westige.utils import *
# from django.db.models import Q
# from decimal import Decimal
# import razorpay
# from razorpay.errors import SignatureVerificationError


class ProductAdd1Serializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields = ["p_id","p_name","mrp_price","discount","total_price","p_description","p_quantity","p_seller","p_image"]
        
        
        

    
class ProductUpdateSerializer(serializers.Serializer):
    p_name=serializers.CharField(required=False)
    p_description= serializers.CharField(required=False)
    mrp_price= serializers.CharField(required=False)
    p_quantity= serializers.CharField(required=False)
    discount= serializers.CharField(required=False)
    total_price= serializers.CharField(required=False)
    p_image=serializers.ImageField(required =False)
    
    
    def update(self, instance, validated_data):
        instance.p_name = validated_data.get("p_name",instance.p_name)
        instance.p_description = validated_data.get("p_description",instance.p_description)
        instance.mrp_price = validated_data.get("mrp_price",instance.mrp_price)
        instance.p_quantity = validated_data.get("p_quantity",instance.p_quantity)
        instance.discount = validated_data.get("discount",instance.discount)
        instance.p_image = validated_data.get("p_image",instance.p_image)
        
        instance.save()
        return instance
    

class ProductGEtSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields = "__all__"
        

class CategoryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = ["id","c_name","c_description"]
        
    def validate(self, attrs):
        c_name=attrs.get("c_name")
        category = Category.objects.filter(c_name=c_name)
        if category :
            raise serializers.ValidationError("this category already available")
            
        return attrs
    
    def update(self, instance, validated_data):
        instance.c_name = validated_data.get("c_name",instance.c_name)
        instance.c_description = validated_data.get("c_description",instance.c_description)
        
        instance.save()
        return instance
    
    
class ReviewAddserializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields = "__all__"