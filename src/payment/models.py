from django.db import models
import uuid
from src.billing.models import BillingModel
from src.user.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from django_countries.fields import CountryField
from src.courses.models import Course


class ContactInfo(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('*Email Address'), null=False)
    name = models.CharField(_('*Name'), max_length=255, blank=True, null=True)
    is_agree = models.BooleanField(
        help_text="I agree to receive instructional and promotional emails. (optional)",
        default=False)

    def __str__(self):
        return self.name


class PaymentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    billing = models.ForeignKey(
        BillingModel, on_delete=models.CASCADE, related_name='billings')

    user = models.ForeignKey(
        BillingModel, on_delete=models.CASCADE, related_name='users', null=True)

    payment_choices = (
        ('P', 'Paypal'),
        ('C', 'Credit or Debit Card'),
    )
    payment_choice = models.CharField(
        choices=payment_choices, max_length=1, null=False)

    contact = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)

    is_paid = models.BooleanField(default=False)

    issued_at = models.DateField(auto_now_add=True)

    expiry_date = models.DateField()

    def save(self, *args, **kwargs):
        days = self.billing.billing_expiry_days
        self.expiry_date = date.now() + timedelta(days=days)
        super(PaymentModel, self).save(*args, **kwargs)

    def __str__(self):
        try:
            return self.user.full_name
        except:
            return self.user.email

    def expiry(self):
        return self.expiry_date

    def billing(self):
        bill = '%s' % (self.billing.title)
        return "Billing :" + bill


class CardModel(models.Model):

    card_name = models.CharField(
        _('*Name on Card'), max_length=255, help_text='Emily J Smith')

    card_number = models.CharField(
        _('*Card Number'), max_length=255, help_text='123 123 421', unique=True)

    expiration_date = models.DateField(_('Expiration Date'))

    cvc_code = models.IntegerField(_('CVC Code'))

    def __str__(self):
        return self.card_name


class ShippingModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    business_name = models.CharField(
        _('Business Name'), max_length=255, blank=True, null=True)

    country = CountryField()

    street_address = models.CharField(_('Street Address'), max_length=255)

    street_address_2 = models.CharField(
        _('Street Address Line 2'), max_length=255, null=True, blank=True)

    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)

    postal_code = models.CharField(
        _('Postal Code'), max_length=255, null=True, blank=True)

    is_same = models.BooleanField(
        _('Delivery address same as billing?'), default=False)

    payment = models.OneToOneField(
        PaymentModel, on_delete=models.CASCADE, related_name='shipping')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Shipping')
        verbose_name_plural = _('Shippings')

    def __str__(self):
        return self.pk


class DeliveryModel(models.Model):
    country = CountryField()

    street_address = models.CharField(_('Street Address'), max_length=255)

    street_address_2 = models.CharField(
        _('Street Address Line 2'), max_length=255, null=True, blank=True)

    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)

    postal_code = models.CharField(
        _('Postal Code'), max_length=255, null=True, blank=True)

    payment = models.OneToOneField(
        PaymentModel, on_delete=models.CASCADE, related_name='delivery')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Delivery')
        verbose_name_plural = _('Deliveries')
