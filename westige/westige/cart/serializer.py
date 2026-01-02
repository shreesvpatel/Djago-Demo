from rest_framework import serializers
from .models import *
from westige.utils import *
from django.db.models import Q



class CartOrWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model= CartAndWishlist
        fields = "__all__"
        
    def validate(self, attrs):
        user=attrs.get("user")
        status=attrs.get("status")
        product=attrs.get("product")
        productfind=CartAndWishlist.objects.filter(user=user,product=product).first()
        item=CartAndWishlist.objects.filter(Q(user=user)&Q(product=product)&Q(status=status)).first()
        if item:
            item.quantity += 1
            item.save()
            attrs["quantity"]=item.quantity
            return attrs
        return attrs
    
class CartOrWishlistUpdateSerializer(serializers.Serializer):
    quantity=serializers.IntegerField()
    
    def update(self, instance, validated_data):    
        item=instance.product.p_quantity
        print("update item for product  =======================>",item)
        quantity = validated_data.get("quantity")
        print("quantity in update ============================>",quantity)
        if not item > quantity :
            print("come in error but not return it ===================#")
            raise serializers.ValidationError(f" only {item} item instock for this product")
        instance.quantity = validated_data.get("quantity",instance.quantity)       
        instance.save()      
        return instance
    
class CartOrWishlistGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= CartAndWishlist
        fields = "__all__"