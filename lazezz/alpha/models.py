import datetime 
from django.db import models

# Create your models here.

class AdminpanelProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    emp_nm = models.CharField(max_length=20)
    emp_id = models.CharField(max_length=30)
    emp_mob = models.IntegerField()
    emp_pass = models.CharField(max_length=20)
    last_login = models.DateTimeField(blank=True, null=True)


class user_account(models.Model):
    name = models.CharField(max_length=100, null = False)
    phone = models.CharField(max_length = 100, primary_key=True)
    password = models.CharField(max_length=100)
    cimg =models.ImageField(max_length=255,null=True)
    total_purchased = models.IntegerField(default = 0)
    last_login = models.DateField(null = True)


class restaurants(models.Model):
    sid  = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=100, null=False)
    oname = models.CharField(max_length=100, null=False, default='NO NAME')
    password = models.CharField(max_length=100, null=False)
    sphone = models.CharField(max_length=10, unique=True, null=False)
    sadd = models.CharField(max_length = 100, null=False)
    aadhaar = models.CharField(max_length=16, unique=True, null=False)
    pan = models.CharField(max_length = 10, unique=True, null = False)
    gstin = models.CharField(max_length=15, unique=True, null=False)
    fssai_no = models.CharField(max_length=14, unique=True, null=False)
    baccno = models.CharField(max_length=16, null=False)
    ifsc = models.CharField(max_length = 10, null=False)
    city = models.CharField(max_length=50, null=False)
    verification = models.IntegerField(default=0)
    o_active = models.IntegerField(default=0)
    t_active = models.IntegerField(default=0)
    rest_img=models.ImageField(max_length=255,null=True)
    r_rate = models.CharField(null=True, max_length=5)
    total_purchased = models.IntegerField(default = 0)
    last_login = models.DateField(null = True)

class foods(models.Model):
    fid = models.AutoField(primary_key=True)
    sid = models.IntegerField()
    fname = models.CharField(max_length=100)
    # fimg = models.ImageField(upload_to='items_image', null=True)
    fimg=models.ImageField(max_length=255,null=True)
    avail = models.IntegerField(default=1)
    price = models.IntegerField(null=False)
    f_rate = models.CharField(null=True, max_length=5)
    # add a rating in rest and foods 2 ccols

class orders(models.Model):
    fid = models.IntegerField()
    quantity=models.IntegerField(default=1)
    sid = models.IntegerField()
    phone = models.CharField(max_length = 10)
    name = models.CharField(max_length=50)
    address = models.CharField(null=True, max_length=255)
    o_active = models.IntegerField(default=0)
    t_active = models.IntegerField(default=0)
    date = models.DateField(default=datetime.datetime.today)


class user_cart(models.Model):
    phone = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    fid = models.IntegerField()
    sid = models.IntegerField()



class user_cart_new(models.Model):
    product=models.IntegerField()
    phone=models.CharField(max_length=11)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.CharField(max_length=100,null=True)
    date=models.DateField(default=datetime.datetime.today)
