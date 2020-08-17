import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from datetime import datetime

from products.models import (
    Nutriment,
    Category,
    Product,
    ProductCategories,
    ProductNutriments,
)

import json
import requests


class Command(BaseCommand):
    help = "Call Open Food Facts API to get products and fill the database"

    def handle(self, *args, **options):

        print("**************************************************")
        print("STARTING DATABASE_UPDATE - {}".format(datetime.now()))
        print("**************************************************")
        for nutriment in settings.NUTRIMENTS:
            if not Nutriment.objects.filter(name__iexact=nutriment):
                print(nutriment)
                new_nutriment = Nutriment(
                    name=nutriment, unit=settings.NUTRIMENTS[nutriment]["unit"]
                )
                new_nutriment.save()
                print("Adding new nutriment to database :", nutriment)
            else:
                print("Existing nutriment :", nutriment)

        print("--------------------------------------------------")
        for category in settings.PRODUCTS_CATEGORIES:
            if not Category.objects.filter(name__iexact=category):
                new_category = Category(name=category)
                new_category.save()
                print("Adding new category to database :", category)
            else:
                print("Existing category :", category)

        print("--------------------------------------------------")
        for category in Category.objects.all():
            self.get_products_for_category(category.name)

        print("**************************************************")
        print("END OF DATABASE_UPDATE - {}".format(datetime.now()))
        print("**************************************************")

        # with open(os.path.join(os.path.dirname(settings.BASE_DIR), 'django_cron.log'), 'a') as log_file:
        #     print("PRODUCTS DATAS UPDATE DONE - {}".format(datetime.now()), file=log_file)


    def get_products_for_category(self, product_category: str):
        """
            GET request to open food fact api to get products in a category.
            For each response, datas are inserted in the database

            Parameters:
                - product_category (str): the name of the category of products to get
        """

        response = self.openfoodfacts_api_get_product(product_category, settings.NB_PRODUCTS_TO_GET, settings.USER_AGENT_OFF)

        for product in response["products"]:

            new_product = Product()
            
            if Product.objects.filter(url__iexact=product["url"]):
                continue
            new_product.url = product["url"]

            # set the image_url of the product
            if ("image_url" in product):
                if Product.objects.filter(image_url__iexact=product["image_url"]):
                    continue                
                new_product.image_url = product["image_url"]

            # set the name of the product
            if "product_name" in product:
                if (
                    product["product_name"] is not None
                    and product["product_name"] is not ""
                ):
                    new_product.name = product["product_name"]
                else:
                    if (
                        product["product_name_fr"] is not None
                        and product["product_name_fr"] is not ""
                    ):
                        new_product.name = product["product_name_fr"]
                    else:
                        continue
            else:
                continue

            # check if product exist in database
            if Product.objects.filter(name__iexact=new_product.name):
                continue

            # set the nutrition score of the product
            if "nutrition_grades_tags" in product:
                if product["nutrition_grades_tags"][0].lower() not in [
                    "a",
                    "b",
                    "c",
                    "d",
                    "e",
                ]:
                    new_product.nutri_score = "e"
                else:
                    new_product.nutri_score = product["nutrition_grades_tags"][
                        0
                    ].lower()

            new_product.save()

            print("Adding new product to database :", new_product.name)

            # create the relations product-category
            if len(product["categories_tags"]) > 0:
                for category in product["categories_tags"]:
                    # parsing of the category tag
                    new_category = category.replace("en:", "")
                    new_category = new_category.replace("fr:", "")

                    if Category.objects.filter(name=new_category):
                        new_product.categories.add(Category.objects.get(name=new_category))
                    else:
                        continue
            else:
                continue

            # create the relations product-nutriment for every nutriments specified in settings
            for nutriment in Nutriment.objects.all():

                if nutriment.name + "_100g" in product["nutriments"]:
                    if product["nutriments"][nutriment.name + "_100g"] is not "":
                        new_product.nutriments.add(
                            nutriment,
                            through_defaults={
                                "quantity": product["nutriments"][nutriment.name + "_100g"]
                            },
                        )
                    else:
                        new_product.nutriments.add(nutriment)
                else:
                    new_product.nutriments.add(nutriment)


    def openfoodfacts_api_get_product(self, category: str, number_of_products: int, user_agent):
        request = requests.get(
            "https://fr-en.openfoodfacts.org/cgi/search.pl?search_terms="
            + category
            + "&page_size="
            + str(number_of_products)
            + "&action=process&json=1",
            headers={"items": user_agent},
        )

        return json.loads(request.text)
