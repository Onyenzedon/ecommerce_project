from django.db import models
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from account.models import CustomUser as User

# Create your models here.

# class CategoryManager(models.Manager):
#     def first(self):
#         return self.all().first()

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=255, unique=True)

    # objects = CategoryManager()

    class Meta:
        # verbose_name = "Product Categories"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, default=Category.objects.all()[0].id)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.IntegerField(null=True, blank=True)
    # image = models.ImageField(upload_to='products/', blank=True, null=True)
    available = models.BooleanField(default=True)
    edited = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def is_available(self):
        if self.in_stock < 1:
            self.available = False
        return self.available

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_values = {field.name: getattr(self, field.name) for field in self._meta.fields} # creates a dictionary of the model fields and their initial values


    def save(self, *args, **kwargs):
        if not self.original_values: #checks if the dictionary is empty or not
            raise ValueError("No initial values!!!")
        for field in self._meta.fields:
            if field.name != 'id' and field.name != 'category' and getattr(self, field.name) != self.original_values[field.name]: # Ensures that the field of id is not included in the comparison
                print("I reached here!!!")
                self.edited = True # flags the instance as edited
                break
            else:
                print("I didn't make it into the block!!!")
        if self.pk:
            if not self.slug:
                self.slug = slugify(self.name)
            original = Product.objects.get(pk=self.pk)
            if original.name != self.name:
                self.slug = slugify(self.name)
                if Product.objects.filter(slug=self.slug).exists(): # checks if an instance with a slug equal to the one formed from the product name already exists 
                    raise ValidationError("Product already exists!!")
        else:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.initial_fields = {}
    #     for field in self._meta.get_fields():
    #         if isinstance(field, models.Field):
    #             self.initial_fields[field.name] = getattr(self, field.name)

    # def save(self, *args, **kwargs):
    #     for field in self._meta.get_fields():
    #         if isinstance(field, models.Field):
    #             initial_value = self.initial_fields.get(field.name)
    #             current_value = getattr(self, field.name)
    #             if initial_value != current_value:
    #                 self.edited = True
    #                 break
    #     super().save(*args, **kwargs)

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products', blank=True, null=True)

    def __str__(self):
        return f"{self.product.name}'s image-{self.id}"


