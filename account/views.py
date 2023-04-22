from django.shortcuts import render,redirect, get_object_or_404, get_list_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, MyLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test




User = get_user_model()
Auth_user = settings.AUTH_USER_MODEL


# Create your views here.

# @user_passes_test(lambda user: user.is_superuser) # serves same purpose as the permission classes in drf(protects a view to a particular set of users)
def register_view(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("Form: ", form)
            form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("main:homepage")
        else:
            messages.error(request, "Invalid Form")
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'accounts_app/register.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print("USER: ", user)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!!!")
            return redirect('main:homepage')
        else:
            print("Invalid user!!!")
            messages.error(request, "Wrong email or password")

    return render(request, 'accounts_app/login.html')

def login_view_func(request):
    print("Request: ", request.GET.get('next'))
    next_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    if request.method == 'POST':
        form = MyLoginForm(request.POST)
        

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            print("Next URL: ", next_url)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!!!")
                return redirect(next_url)
            else:
                messages.error(request, "No user with these credentials")
        else:
            print("Invalid form: ", form.errors)
            messages.error(request, "Invalid form rendered")

    else:
        form = MyLoginForm()

    context = {
        'form': form
    }

    return render(request, 'accounts_app/login2.html', context)

def logout_view(request):
    logout(request)
    return redirect('main:homepage')

def deactivate_user(request):
    user = request.user
    user_id = user.id
    user = get_object_or_404(User, id=user_id)

    if user.is_authenticated:
        user.is_active = False
        messages.success(request, "Account successfully deactivated!!!")
        return redirect("homepage")
    else:
        messages.warning("You are not logged in to access this page. Please log in.")
        return redirect("login")
       

def delete_user(request):
    user = request.user
    user_id = user.id
    user = get_object_or_404(User, id=user_id)
    try:
        user.delete()
    except:
        messages.error(request,'Please try again.')
        return redirect('homepage')

    messages.success(request, 'Profile successfully deleted.')
    return redirect('homepage')

