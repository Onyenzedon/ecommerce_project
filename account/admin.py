from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from account.models import CustomUser
from account.forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.translation import gettext_lazy as _
# Register your models here.


class CustomUserAdmin(BaseAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (_("User Information"), {'fields': ('email', 'password', 'slug')},),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    ''' list_display = ("email", "date_joined", "last_login")
    search_fields = ("email",)
    list_filter = ("last_login",)
    
    ordering = ("email",)
    
    add_fieldsets = (
         (
             None,
             {
                 "classes": ("wide",),
                 "fields": ("email", "password1", "password2"),
             },
         ),
     )
    
    fieldsets = (
          (None, {"fields": ("email", "password")}),
          (_("Personal info"), {"fields": ("email",)}),
          (
             _("Permissions"),
             {
                 "fields": (
                     "is_active",
                     "is_staff",
                     "is_superuser",
                     "groups",
                     "user_permissions",
                 ),
             },
         ),
         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
     )
'''


admin.site.register(CustomUser, CustomUserAdmin)
