from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [    
    path('', views.HomeView.as_view(), name='home'),
    path('user/', views.UserView.as_view(), name='user'),
    path('user/login', views.UserLogin.as_view(), name='login'),
    path('user/logout', views.UserLogout.as_view(), name='logout'),
    path('user/sign-up', views.UserCreate.as_view(), name='user-create'),
    path('search-results/', views.SearchResult.as_view(), name='product-search-results'),
    path('user-save-product/<int:product_id>', views.UserSaveProduct.as_view(), name='save-product'),
    path('user-results/', views.UserResults.as_view(), name='product-user-results'),
    path('details/<int:product_id>', views.ProductDetails.as_view(), name='product-details'),
]