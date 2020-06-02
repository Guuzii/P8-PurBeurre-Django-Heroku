from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from .models import Nutriment, Category, Product, ProductCategories, ProductNutriments, ProductUsers

class ProductCategoriesInline(admin.TabularInline):
    model = Product.categories.through # the query goes through an intermediate table.
    extra = 1
    verbose_name = "Catégorie produit"
    verbose_name_plural = "Catégories produit"
    readonly_fields = ["category"]

class ProductNutrimentsInline(admin.TabularInline):
    model = Product.nutriments.through # the query goes through an intermediate table.
    extra = 1
    verbose_name = "Nutriment produit"
    verbose_name_plural = "Nutriments produit"
    readonly_fields = ["nutriment", "quantity"]

class ProductUsersInline(admin.TabularInline):
    model = Product.users.through # the query goes through an intermediate table.
    extra = 1
    verbose_name = "Utilisateur produit"
    verbose_name_plural = "Utilisateurs produit"
    # readonly_fields = ["nutriment", "quantity"]

@admin.register(Nutriment)
class NutrimentAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    readonly_fields = ["name", "unit"]

    def has_add_permission(self, request):
        return False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    readonly_fields = ["name"]

    def has_add_permission(self, request):
        return False

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductCategoriesInline, ProductNutrimentsInline, ProductUsersInline]
    search_fields = ['name',]
    list_filter = ['nutri_score', 'categories',]

    def has_add_permission(self, request):
        return False