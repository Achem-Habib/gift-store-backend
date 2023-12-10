from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import (Category, Occasion, Product, RecipientType, Review,
                     Subcategory)
from .serializers import (CategoryAndSubcategorySerializer, CategorySerializer,
                          OccasionSerializer, ProductSerializer,
                          RecipientSerializer, ReviewSerializer,
                          SubcategorySerializer)


# views for getting all categories and subcategories
@api_view(['GET'])
def get_all_categories_subcategories(request):
    categories = Category.objects.all()
    serializer = CategoryAndSubcategorySerializer(categories, many=True)
    return Response(serializer.data)


# views for getting all categories
@api_view(['GET'])
def get_all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# getting the subcategories list under a specified category
class SubcategoriesByCategory(ListAPIView):
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        # Extract category_slug from URL
        category_slug = self.kwargs['category_slug']
        return Subcategory.objects.filter(category__slug=category_slug)


# featured products views
@api_view(['GET'])
def get_featured_products(request):
    featured_products = Product.objects.filter(featured=True)
    serializer = ProductSerializer(featured_products, many=True)
    return Response(serializer.data)


# getting all occasion list
@api_view(['GET'])
def get_all_occasions(request):
    occasions = Occasion.objects.all()
    serializer = OccasionSerializer(occasions, many=True)
    return Response(serializer.data)

# getting all occasion list


@api_view(['GET'])
def get_all_recipients(request):
    recipients = RecipientType.objects.all()
    serializer = RecipientSerializer(recipients, many=True)
    return Response(serializer.data)


# getting all the products
class AllProducts(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


# getting the product list by category
class ProductsByCategory(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Extract category_slug from URL
        category_slug = self.kwargs['category_slug']
        return Product.objects.filter(subcategory__category__slug=category_slug)


# getting the product list by sub category
class ProductsBySubcategory(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Extract subcategory_slug from URL
        subcategory_slug = self.kwargs['subcategory_slug']
        return Product.objects.filter(subcategory__slug=subcategory_slug)


# get single product
@api_view(['GET'])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)


# getting all reviews for a single product
@api_view(['GET'])
def get_reviews(request, product_slug):
    try:
        reviews = Review.objects.filter(product__slug=product_slug)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Reviews not found'}, status=404)



@api_view(['POST'])
def submit_review(request):
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
