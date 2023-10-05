from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to="categories/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Occasion(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to="occassions/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class RecipientType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to="recipients/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Product(models.Model):
    # relations to other model
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    occasions = models.ManyToManyField(Occasion, blank=True)
    recipient_types = models.ManyToManyField(RecipientType, blank=True)

    # product information
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField()
    featured = models.BooleanField(default=False)

    # images
    primary_image = models.ImageField(
        upload_to='product_primary_images/', blank=True)
    more_images = models.ManyToManyField(
        Image, blank=True, related_name='products')

    # date and time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
