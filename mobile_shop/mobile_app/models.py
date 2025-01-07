from django.db import models
from django.contrib.auth.models import User
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
