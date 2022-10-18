from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Product(models.Model):
    Product_Id = models.AutoField
    Product_Name = models.CharField(max_length=50)
    Category = models.CharField(max_length=50)
    Price = models.IntegerField()
    Description = models.TextField(max_length=1000)
    Publish_Date = models.DateField()
    Image = models.ImageField(upload_to="")
    Out_Of_Stock = "Out Of Stock"
    In_Stock = "Available"
    Choices = [
        (In_Stock, "Available"),
        (Out_Of_Stock, "Out Of Stock")
    ]
    Stock_Details = models.CharField(max_length=12, choices=Choices, default="Available")

    def __str__(self) -> str:
        return self.Product_Name

class Message(models.Model):
    Message_Id = models.AutoField
    Email = models.EmailField()
    Username = models.CharField(max_length=50)
    Phone = PhoneNumberField(default="")
    Query = models.TextField(max_length=1000)

    def __str__(self) -> str:
        return self.Username

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    Items = models.TextField(max_length=1400)
    Email = models.EmailField(default="")
    First_name = models.CharField(max_length=33)
    Last_name = models.CharField(max_length=33)
    Username = models.CharField(max_length=33)
    Address_1 = models.TextField(max_length=1000)
    Address_2 = models.TextField(max_length=1000)
    State = models.CharField(max_length=24)
    City = models.CharField(max_length=24)
    Zip_Code = models.CharField(max_length=6)
    Phone = PhoneNumberField()
    Amount = models.CharField(max_length=14,default=0)
    Json = models.CharField(max_length=1400, default="")

    def __str__(self) -> str:
        return f"Order Number {self.order_id}"

class Order_Update(models.Model):
    Update_Id = models.AutoField(primary_key=True)
    Order_Id = models.IntegerField(default="")
    Update = models.TextField(max_length=6000)

    def __str__(self) -> str:
        return self.Update[0:14] + "..."

class Review(models.Model):
    User = models.ForeignKey(User, models.CASCADE)
    Product = models.ForeignKey(Product, models.CASCADE)
    Review = models.TextField(max_length=250)
    Rating = models.CharField(default=0, max_length=12)
    Date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.User}'s Review for {self.Product}"

