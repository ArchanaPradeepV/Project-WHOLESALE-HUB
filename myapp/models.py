from django.db import models

# Create your models here.
class login_tb(models.Model):
    Username=models.CharField(max_length=100)
    Password=models.CharField(max_length=100)
    Type=models.CharField(max_length=100)

class staff_tb(models.Model):
    Loginid=models.ForeignKey(login_tb,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    Place=models.CharField(max_length=100)
    PhoneNo=models.BigIntegerField()
    Email=models.CharField(max_length=100)
    Image=models.FileField()

class retailer_tb(models.Model):
    Loginid=models.ForeignKey(login_tb,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    Place=models.CharField(max_length=100)
    PhoneNo=models.BigIntegerField()
    Email=models.CharField(max_length=100)
    Image=models.FileField()

class category_tb(models.Model):
    Category=models.CharField(max_length=100)
    Description=models.CharField(max_length=100)

class product_tb(models.Model):
    Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=100)
    Categoryid = models.ForeignKey(category_tb,on_delete=models.CASCADE)
    Price = models.FloatField()
    Stock = models.BigIntegerField()

class order_tb(models.Model):
    Retailerid=models.ForeignKey(retailer_tb,on_delete=models.CASCADE)
    Amount=models.FloatField()
    Date=models.DateField()
    Status=models.CharField(max_length=100)

class orderdetails_tb(models.Model):
    Orderid=models.ForeignKey(order_tb,on_delete=models.CASCADE)
    Productid = models.ForeignKey(product_tb,on_delete=models.CASCADE)
    Price=models.FloatField()
    Quantity=models.FloatField()
    Status=models.CharField(max_length=100)

class payment_tb(models.Model):
    Orderid=models.ForeignKey(order_tb,on_delete=models.CASCADE)
    Date = models.DateField()
    Status = models.CharField(max_length=100)

class return_tb(models.Model):
    Orderid=models.ForeignKey(order_tb,on_delete=models.CASCADE)
    Date = models.DateField()
    Status = models.CharField(max_length=100)
    Reason=models.CharField(max_length=100)
