from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Disease(models.Model):
    plant_name = models.CharField(max_length=50)
    disease_name = models.CharField(max_length=100)
    detail = models.TextField()
    solution = models.TextField()
    reference = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plant_name + ' ' + self.disease_name

class TeamMember(models.Model):
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    member_image = models.TextField()
    quote = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    msg = models.TextField()
    msg_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    rating = models.DecimalField(max_digits=4, decimal_places=2, validators=[
        MaxValueValidator(10),
        MinValueValidator(0)
        ]),
    comment = models.TextField(max_length=150)
    review_dt = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class Subscriber(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    #subscription_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email




