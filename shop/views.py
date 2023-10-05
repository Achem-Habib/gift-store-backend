from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Occasion, Product, RecipientType
from .serializers import (CategorySerializer, OccasionSerializer,
                          ProductSerializer, RecipientSerializer,
                          SubCategorySerializer)


@api_view(['GET'])
def get_all_categories(request):
    top_level_categories = Category.objects.filter(
        parent_category__isnull=True)
    serializer = CategorySerializer(top_level_categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_subcategories(request):
    subcategories = Category.objects.filter(parent_category__isnull=False)
    serializer = SubCategorySerializer(subcategories, many=True)
    return Response(serializer.data)


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


# getting the product list by category
class ProductListByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']

        if category_slug == "all":
            return Product.objects.all()

        else:
            try:
                # Get the category based on the provided slug
                category = Category.objects.get(slug=category_slug)

                # Build a query to fetch products for the category and its subcategories
                query = Q(category=category)

                def add_subcategories_to_query(cat):
                    subcategories = cat.subcategories.all()
                    if subcategories:
                        for subcategory in subcategories:
                            query.add(Q(category=subcategory), Q.OR)
                            add_subcategories_to_query(subcategory)

                add_subcategories_to_query(category)

                return Product.objects.filter(query)

            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Category does not exist'}, status=404)
