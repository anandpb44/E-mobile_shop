from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
from datetime import timedelta
# Create your models here.
class Category(models.Model):
    cname=models.TextField()
class Product(models.Model):
    pid=models.TextField()
    pname=models.TextField()
    pdis=models.TextField()
    img=models.FileField()
    cate=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    
class Details(models.Model):
    color=models.TextField()
    price=models.TextField()
    stock=models.TextField()
    storage=models.TextField()
    ram=models.TextField()
    img=models.FileField()
    pro=models.ForeignKey(Product,on_delete=models.CASCADE)

class Cart(models.Model):
    details=models.ForeignKey(Details,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    phn=models.IntegerField()
    house=models.TextField()
    street=models.TextField()
    pin=models.IntegerField()
    state=models.TextField()

class Buy(models.Model):
    product=models.ForeignKey(Details,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    qty=models.IntegerField()
    t_price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    delivery_date = models.DateField(null=True, blank=True)

    def set_delivery_date(self):
        """Set a default delivery date based on acceptance."""
        if self.is_accepted:
            self.delivery_date = self.date + timedelta(days=7)  # Example: 7 days after acceptance
            self.save()

class Order(models.Model):
    name=CharField(_("customer Name"),max_length=254,blank=False,null=False)
    amount=models.FloatField(_("Amount"),null=False,blank=False)
    status=CharField(_("Payment Status"),default=PaymentStatus.PENDING,max_length=254,blank=False,null=False)
    provider_order_id=models.CharField(_("Order ID"),max_length=40,null=False,blank=False)
    payment_id=models.CharField(_("Payment ID"),max_length=36,null=False,blank=False)
    signature_id=models.CharField(_("Signature ID"),max_length=128,null=False,blank=False)
    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"