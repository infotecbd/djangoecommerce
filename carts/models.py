from django.db import models

from accounts.models import CustomUser
from products.models import Product, TimeStampedModel
from django.contrib.auth.models import User
from django.conf import settings



class Cart(TimeStampedModel):
    session_key = models.CharField(max_length=250)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.session_key


class CartItem(TimeStampedModel):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,  # allow nulls temporarily
    blank=True  # optional, for admin/forms
)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    def sub_total(self):
        return self.product.discount_price * self.quantity

    def __str__(self):
        return f"CartItem: {self.product.name}"


