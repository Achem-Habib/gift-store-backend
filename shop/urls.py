from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    # Get all top-level categories
    path('categories/', views.get_all_categories, name='category-list'),

    # Get all sub categories
    path('subcategories/', views.get_all_subcategories, name='subcategory-list'),

    # Get all occassions list
    path('occasions/', views.get_all_occasions, name="occasions"),

    # Get all recipient types list
    path('recipients/', views.get_all_recipients, name="recipients"),

    # Get all sub categories
    path('featured-products/', views.get_featured_products,
         name='featured-products'),

    # Get all the products under a specific category
    path('category/<str:category_slug>/',
         views.ProductListByCategory.as_view(), name='product-list-by-category'),


]
