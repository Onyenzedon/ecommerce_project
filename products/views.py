from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from products.models import Category, Product, Image
from .forms import ProductForm, ImageForm

products = Product.objects.all()




def all_products(request, slug=None):
    if not slug:
        categories = Category.objects.all()
        products = Product.objects.all()
        images = Image.objects.filter(product__in=products)
        first_image = images.first()
        context = {
            "products": products,
            "images": images,
            "first_image":first_image,
            'categories':categories
        }
        template_name = "products/all_products2.html"
    else:
        product = Product.objects.get(slug=slug)
        images = Image.objects.filter(product=product)
        print("Images: ", images)
        # images = product.images.all()
        
        context = {
            "product": product,
            "product_detail": product.name + " detail",
            'images': images
        }
        template_name = "products/product_detail.html"
    return render(request, template_name, context)

def product_detail(request):
    return HttpResponse("Product details")

def create_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        # image_form = ImageForm(request.POST, request.FILES)
        # formset = ImageFormSet(request.POST, request.FILES, instance=form.instance)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.created_by = request.user
            product.save()

            images = request.FILES.getlist('images')
            for image in images:
                Image.objects.create(product=product, image=image)

            return redirect('products:product_detail', slug=product.slug)
    else:
        product_form = ProductForm()

    context = {
        'product_form': product_form
        }

    return render(request, 'products/create-product.html', context)

def update_product(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        # image_form = ImageForm(request.POST, request.FILES)
        # formset = ImageFormSet(request.POST, request.FILES, instance=form.instance)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.created_by = request.user
            product.save()

            images = request.FILES.getlist('images')
            for image in images:
                Image.objects.create(product=product, image=image)

            return redirect('products:product_detail', slug=product.slug)
    else:
        product_form = ProductForm(instance=product)

    context = {
        'product_form': product_form
        }

    return render(request, 'products/update-product.html', context)

