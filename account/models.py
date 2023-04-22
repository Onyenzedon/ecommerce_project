from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.text import slugify

from .managers import CustomUserManager

# Create your models here.
       
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = None
    email = models.EmailField(_('email address'), unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        # db_table = 'auth_user'
        verbose_name = "User"
        verbose_name_plural = "Users" 

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        title = self.email.split("@")[0]
        if not self.slug:
            self.slug = slugify(title)
        slug_count = 1
        while CustomUser.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug = f"{slugify(self.title)}-{slug_count}"
            slug_count += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email



