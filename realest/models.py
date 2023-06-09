from django.db import models


# Create your models here.

class property(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=50)
    propertytype = models.CharField(max_length=40)
    foor = models.CharField(max_length=10)
    project = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,null=True)
    bhk = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    floor = models.CharField(max_length=10)
    date = models.DateField()
    type = models.CharField(max_length=20)
    price = models.CharField(max_length=100)
    deposite = models.CharField(max_length=100,null=True)
    img = models.ImageField(null=True , blank=True , upload_to='images/')

class person(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    mail = models.EmailField()
    phone = models.BigIntegerField()


    
    
    