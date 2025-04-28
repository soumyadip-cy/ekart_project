from django.db import models
from django.contrib.auth.models import User, auth
from datetime import datetime, timedelta

class Categories(models.Model):
    cat_name=models.CharField(max_length=100)
    cat_pic=models.ImageField(upload_to="cat_images/")
    class Meta():
        db_table="Categories"

class Types(models.Model):
    type_name=models.CharField(max_length=100)
    type_pic=models.ImageField(upload_to="type_images/")
    cat_fk=models.ForeignKey(Categories, on_delete=models.CASCADE)
    class Meta():
        db_table="Types"

class Brands(models.Model):
    brand_name=models.CharField(max_length=100)
    class Meta():
        db_table="Brands"

class Products(models.Model):
    name=models.CharField(max_length=100)
    desc=models.TextField(max_length=500)
    price=models.IntegerField()
    brand_fk=models.ForeignKey(Brands,on_delete=models.CASCADE)
    type_fk=models.ForeignKey(Types,on_delete=models.CASCADE)
    class Meta():
        db_table="Products"

class Images(models.Model):
    product_image=models.ImageField(upload_to="product_images/")
    product_fk=models.ForeignKey(Products, on_delete=models.CASCADE)
    yes='Y'
    no='N'
    condition=[(yes,'YES'),(no,'NO')]
    main_img=models.CharField(choices=condition,max_length=10,default=no)
    class Meta():
        db_table="Images"

class Reviews(models.Model):
    review_text=models.CharField(max_length=500)
    product_fk=models.ForeignKey(Products, on_delete=models.CASCADE)
    user_fk=models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta():
        db_table="Reviews"

class ActualStock(models.Model):
    act_quant=models.IntegerField()
    product_fk=models.ForeignKey(Products, on_delete=models.CASCADE)
    class Meta():
        db_table="ActualStock"

class TempStock(models.Model):
    temp_quant=models.IntegerField()
    product_fk=models.ForeignKey(Products, on_delete=models.CASCADE)
    class Meta():
        db_table="TempStock"

class Carts(models.Model):
    id=models.AutoField(primary_key=True)
    product_fk=models.ForeignKey(Products , on_delete=models.CASCADE)
    user_fk=models.ForeignKey(User , on_delete=models.CASCADE)
    num=models.IntegerField()
    price=models.IntegerField()
    class Meta():
        db_table="Carts"

class Orders(models.Model):
    product_fk=models.ForeignKey(Products , on_delete=models.CASCADE)
    user_fk=models.ForeignKey(User , on_delete=models.CASCADE)
    num=models.IntegerField()
    price=models.IntegerField()
    ord_time=models.DateTimeField(auto_now_add=True)
    exp_ship_time=models.DateField(default=datetime.now()+timedelta(days=7))
    class Meta():
        db_table="Orders"

class Shipping(models.Model):
    yes='Y'
    no='N'
    ship_cond=[(yes,'YES'),(no,'NO')]
    order_id=models.ForeignKey(Orders, on_delete=models.CASCADE)
    shipping_status=models.CharField(choices=ship_cond,max_length=10, default=no)
    class Meta():
        db_table="Shipping"

class Addresses(models.Model):
    user_fk=models.ForeignKey(User ,on_delete=models.CASCADE)
    address=models.CharField(max_length=500)
    class Meta():
        db_table="Addresses"

class OrderAddresses(models.Model):
    order_id=models.ForeignKey(Orders, on_delete=models.CASCADE)
    address_id=models.ForeignKey(Addresses, on_delete=models.CASCADE)
    class Meta():
        db_table="OrderAddresses"

class Highlighted_Products(models.Model):
    id = models.AutoField(primary_key=True)
    product_fk=models.ForeignKey(Products, on_delete=models.CASCADE)
    class Meta():
        db_table="Highlighted_Products"