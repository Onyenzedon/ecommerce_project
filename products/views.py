from django.shortcuts import render, redirect
from django.http import HttpResponse
from products.models import Category, Product, Image
from .forms import ProductForm, ImageForm

products = Product.objects.all()




def all_products(request, slug=None):
    if not slug:
        products = Product.objects.all()
        images = Image.objects.filter(product__in=products)
        first_image = images.first()
        context = {
            "products": products,
            "images": images,
            "first_image":first_image
        }
        template_name = "products/all_products.html"
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
        image_form = ImageForm(request.POST, request.FILES)
        # formset = ImageFormSet(request.POST, request.FILES, instance=form.instance)

        if product_form.is_valid() and image_form.is_valid():
            product = product_form.save(commit=False)
            product.created_by = request.user

            product.save()
            print("Image form: ", image_form)

            images = image_form.cleaned_data.get('image')
            for image in images:
                Image.objects.create(product=product, image=image)

            return redirect('products:product_detail', slug=product.slug)
    else:
        product_form = ProductForm()
        image_form = ImageForm()

    context = {
        'product_form': product_form, 
        'image_form': image_form
        }

    return render(request, 'products/create-product.html', context)

def update_product(request, slug, id):
    product = Product.objects.get(slug=slug, id=id)
    images = Image.objects.filter(product=product)

    if not images:
        blank_image = Image(product=product)
        images = [blank_image]

    if images:
        for i in images:
            if i.image:
                print("Image: ", i.image.url)
            else:
                print("No image url")
        # print("There are images")
    else:
        print("There are no images")

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        image_forms = [ImageForm(request.POST, request.FILES, instance=image) for image in images]
        # formset = ImageFormSet(request.POST, request.FILES, instance=form.instance)


        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.created_by = request.user

            product.save()
            print("Image form: ", image_forms)

            # images = request.FILES.getlist("image")
            for image_form in image_forms:
                if image_form.is_valid():
                    image_form.save()

            return redirect('products:product_detail', slug=product.slug)
    else:
        product_form = ProductForm(instance=product)
        image_form = [ImageForm(instance=image) for image in images]

    context = {
        'product_form': product_form, 
        'image_form': image_form
        }

    return render(request, 'products/update-product.html', context)

