from django.db import models
from westige.models import UserMaster,CartAndWishlist
from westige.product.models import Products

# class CartAndWishlist(models.Model):
#     STATUS_CHOICES = (
#         ("cart", "Cart"),
#         ("wishlist", "Wishlist"),
#     )

#     user = models.ForeignKey(UserMaster, on_delete=models.CASCADE,related_name="user")
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)

#     class Meta:
#         unique_together = ("user", "product", "status")

#     def __str__(self):
#         return f"{self.user.email} - {self.product.p_name}"