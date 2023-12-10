from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    # Get all categories and subcategories
    path('categories-subcategories/',
         views.get_all_categories_subcategories, name='category-subcategory-list'),

    # Get all categories
    path('categories/',
         views.get_all_categories, name='category-list'),

    # Get all subcategories under a specified category
    path('subcategories-by-category/<str:category_slug>',
         views.SubcategoriesByCategory.as_view(), name='subcategories-by-category'),


    # Get all occassions list
    path('occasions/', views.get_all_occasions, name="occasions"),

    # Get all recipient types list
    path('recipients/', views.get_all_recipients, name="recipients"),

    # Get featured products
    path('featured-products/', views.get_featured_products,
         name='featured-products'),

    # Get all the products
    path('all-products/', views.AllProducts.as_view(), name='all-products'),

    # Get the products under a specific category
    path('category/<str:category_slug>/',
         views.ProductsByCategory.as_view(), name='products-by-category'),

    # Get the products under a specific category
    path('subcategory/<str:subcategory_slug>/',
         views.ProductsBySubcategory.as_view(), name='products-by-subcategory'),

    # Get single product detail
    path('products/<slug:slug>/', views.product_detail, name='product-detail'),

    # Get all the reviews for a single product
    path('reviews/<slug:product_slug>/', views.get_reviews, name='reviews'),

    # Submit the review
    path('submit-review/', views.submit_review, name='submit_review'),



]
