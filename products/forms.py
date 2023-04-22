from django.forms.models import inlineformset_factory
from django import forms
from django.forms import inlineformset_factory
from .models import Product, Category, Image


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

# class ProductForm(forms.ModelForm):
#     images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

#     class Meta:
#         model = Product
#         fields = ['name', 'category', 'description', 'price', 'in_stock']

# class ImageForm(form.ModelForm):

#     class Meta:
#         model = Image
#         fields = ("image",)


# class ProductForm(forms.ModelForm):
#     images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

#     class Meta:
#         model = Product
#         fields = ['category', 'name', 'description', 'price', 'in_stock']

# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'description', 'price', 'in_stock')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

# ImageFormSet = inlineformset_factory(Product, Image, fields=('image',), extra=3)


