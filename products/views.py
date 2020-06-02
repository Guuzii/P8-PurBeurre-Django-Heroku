# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.conf import settings
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from products.models import Nutriment, Category, Product, ProductCategories, ProductNutriments, ProductUsers
from products.forms import SearchForm, UserCreateForm, LoginForm

# Create your views here.
class HomeView(View):
    template_name = 'products/homepage.html'
    context = {
        'search_form': SearchForm()
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class UserView(View):
    template_name = 'products/user-details.html'
    context = {
        'search_form': SearchForm()
    }

    def get(self, request):
        self.context['title'] = 'Salut ' + request.user.first_name + ' !'
        self.context['user'] = request.user
        return render(request, self.template_name, self.context)


class UserLogin(LoginView):
    template_name = 'products/user-login.html'
    authentication_form = LoginForm
    extra_context = {
        'title': 'Connexion utilisateur',
        'search_form': SearchForm()
    }


class UserLogout(LogoutView):
    def get(self, request, *args, **kwargs):
        return redirect('home')


class UserCreate(View):
    template_name = 'products/user-create.html'
    context = {
        'title': 'Création utilisateur',
        'search_form': SearchForm()
    }

    def get(self, request):
        """Return the signup template"""
        form = UserCreateForm()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request):
        """Process the UserCreate form, redirect and log the user if it is
        valid, return the signup template otherwise"""
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else :
            self.context['form'] = form
            self.context['errors'] = form.errors.items()
            return render(request, self.template_name, self.context)


class SearchResult(View):
    template_name = 'products/result-search.html'
    context = {
        'search_form': SearchForm()
    }
    
    def post(self, request):
        form = SearchForm(request.POST)

        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            searched_product = Product.objects.filter(name__icontains=product_name).first()
            saved_product = []

            if searched_product:
                substitutes_products = Product.objects.filter(categories=searched_product.categories.first()).exclude(id=searched_product.id).order_by('nutri_score')[:12]
                
                if request.user.is_authenticated:
                    if ProductUsers.objects.filter(product=searched_product, user=request.user).exists():
                        saved_product.append(searched_product)

                    for product in substitutes_products:
                        if ProductUsers.objects.filter(product=product, user=request.user).exists():
                            saved_product.append(product)
            else:
                substitutes_products = None    

            self.context['title'] = 'produit trouvé pour la recherche : "' + product_name + '"'
            self.context['searched_product'] = searched_product
            self.context['products'] = substitutes_products
            self.context['saved_product'] = saved_product

            return render(request, self.template_name, self.context)
        else:
            self.context['errors'] = form.errors.items()
            return render(request, 'products/homepage.html', self.context)


class ProductDetails(View):
    context = {
        'search_form': SearchForm()
    }

    def get(self, request, product_id):
        searched_product = get_object_or_404(Product, id=product_id)
        product_nutriments = searched_product.nutriments.all()
        clean_nutriments = []

        for nutriment in product_nutriments:
            clean_nutriments.append({
                "name": settings.NUTRIMENTS[nutriment.name]['name'],
                "unit": nutriment.unit,
                "quantity": ProductNutriments.objects.filter(product=searched_product, nutriment=nutriment).first().quantity
            }) 

        self.context['title'] = searched_product.name
        self.context['searched_product'] = searched_product
        self.context['product_nutriments'] = clean_nutriments

        return render(request, 'products/product-details.html', self.context)


class UserResults(View):
    template_name = 'products/result-user.html'
    context = {
        'search_form': SearchForm()
    }

    def get(self, request):
        product_users_list = ProductUsers.objects.filter(user=request.user)
        product_list = []

        for queryset in product_users_list:
            product_list.append(queryset.product)

        self.context['title'] = 'Salut ' + request.user.first_name + ' !'
        self.context['products'] = product_list
        return render(request, self.template_name, self.context)


class UserSaveProduct(View):
    context = {
        'search_form': SearchForm()
    }
    
    def get(self, request, product_id):
        product_to_save = Product.objects.get(id=product_id)

        if not ProductUsers.objects.filter(product=product_to_save, user=request.user).exists():
            product_user_relation = ProductUsers(product=product_to_save, user=request.user)
            product_user_relation.save()
            data = {
                'saved': True,
                'product_name': product_to_save.name,
                'response': "ajouté à vos favoris"
            }
        else:
            ProductUsers.objects.filter(product=product_to_save, user=request.user).delete()
            data = {
                'saved': False,
                'product_name': product_to_save.name,
                'response': "retiré de vos favoris"
            }

        return JsonResponse(data)
        