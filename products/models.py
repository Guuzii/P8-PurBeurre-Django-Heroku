from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Nutriment(models.Model):
    name = models.CharField("Nom", max_length=255, unique=True)
    unit = models.CharField("Unité de mesure", max_length=2)

    class Meta:
        verbose_name = "Nutriment"
        verbose_name_plural = "Nutriments"

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField("Nom", max_length=255, unique=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("Nom", max_length=255, unique=True)
    url = models.URLField("Url vers la page OpenFoodFact", max_length=255, unique=True)
    image_url = models.URLField("Url de l'image", max_length=255, unique=True, null=True)
    nutri_score = models.CharField("Score nutritionnel", max_length=1)
    nutriments = models.ManyToManyField('products.Nutriment', through='products.ProductNutriments')
    categories = models.ManyToManyField('products.Category', through='products.ProductCategories')
    users = models.ManyToManyField(get_user_model(), through='products.ProductUsers')

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.name

class ProductNutriments(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    nutriment = models.ForeignKey('products.Nutriment', on_delete=models.CASCADE)
    quantity = models.FloatField("Quantité", null= True)

class ProductCategories(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    category = models.ForeignKey('products.Category', on_delete=models.CASCADE)

class ProductUsers(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)