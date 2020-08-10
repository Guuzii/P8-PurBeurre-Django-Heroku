from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from products.models import (
    Nutriment,
    Category,
    Product,
    ProductCategories,
    ProductNutriments,
)


class Command(BaseCommand):
    help = "Delete all datas in all tables from the database"

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Nutriment.objects.all().delete()
        Category.objects.all().delete()
        ProductNutriments.all().delete()
        ProductCategories.all().delete()

        self.stdout.write("DATABASE RESET FINISHED")

