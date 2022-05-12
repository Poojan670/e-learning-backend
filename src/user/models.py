from django.db import models
import uuid
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


def user_directory_path(instance, filename):
    return "users/{}/{}".format(instance.email, filename)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, full_name, ** other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
        if not password:
            raise ValueError(_('Password is not set'))
        email = self.normalize_email(email)
        user = self.model(email=email, password=password,
                          full_name=full_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, full_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))

        if other_fields.get('is_superuser') is not True and other_fields.get('is_active') is not True:
            raise ValueError(
                _('Superuser must be assigned to is_superuser=True and should be active'))

        user = self.create_user(email, password, full_name, ** other_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name=_('email address'), unique=True,
                              null=False, blank=False, help_text="Please enter your email address..")
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'NaN'
    gender_choices = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Rather not say')
    )
    gender = models.CharField(choices=gender_choices,
                              max_length=3, default=OTHER)
    full_name = models.CharField(verbose_name=_('Full Name'), max_length=60,
                                 blank=False, null=True, help_text="Please enter your full nmae")
    is_active = models.BooleanField(_('is_verified'), default=False)
    otp = models.IntegerField(null=True, blank=True)
    activation_key = models.CharField(
        max_length=150, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=user_directory_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    username = None
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['gender', 'full_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = '%s' % (self.full_name)
        return full_name


class DeactivateUser(models.Model):
    user = models.OneToOneField(
        User, related_name="deactivate", on_delete=models.CASCADE
    )
    deactive = models.BooleanField(default=True)

    deactivated_at = models.DateTimeField(auto_now_add=True)
