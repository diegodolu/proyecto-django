from django.db import models

class Distributor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

class Brand(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    distributors = models.ManyToManyField(Distributor, through='DistributorBrand')

class DistributorBrand(models.Model):
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

class Sensor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='sensors', on_delete=models.CASCADE)

class Purchase(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.IntegerField()

class Reading(models.Model):
    id = models.IntegerField(primary_key=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    reading_date = models.DateTimeField()
    gas_percentage = models.IntegerField()