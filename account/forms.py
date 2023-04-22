from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import EmailValidator

from .models import CustomUser

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',label_suffix = '', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id':'password1'}))
    password2 = forms.CharField(label='Password Confirmation', label_suffix = '', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id':'password2'}))

    class Meta:
        model = CustomUser
        fields = ('email', )
        label_suffix = ''
        labels = {
            'email': 'Your Email',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'id':'email','class': 'form-control form-control-lg'})
        }

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class MyLoginForm(forms.ModelForm):
    # username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password')

    # def clean(self):
    #     print("Cleaned_data: ", self.cleaned_data)
    #     email = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")

    #     if email and password:
    #         try:
    #             user = User.objects.get(email=email)
    #         except User.DoesNotExist:
    #             raise forms.ValidationError("Invalid email or password")
    #         else:
    #             print("User.check_password: ", user.check_password(password))
    #             if not user.checkpassword(password):
    #                 raise forms.ValidationError("Invalid email or password")

    #         self.cleaned_data["user"] = user

    #     return self.cleaned_data

    def clean(self):
        # cleaned_data = super().clean()
        # email = cleaned_data['email']
        # password = cleaned_data['password']

        # # validator = EmailValidator()

        # # if not password:
        # #     raise forms.ValidationError("Please provide password")

        # # if len(password) < 4:
        # #     raise forms.ValidationError("Password too short. Must not be less than four characters")

        # # if not email:
        # #     raise forms.ValidationError("Email is required")

        # # try:
        # #     validator(email)
        # # except forms.ValidationError:
        # #     raise forms.ValidationError('Invalid email address provided')

        # # return self.cleaned_data

        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError("Invalid credentials")

            


    # class Meta:
    #     model = CustomUser
    #     fields = ('username', 'password')

        # USERNAME_FIELD = 'email'