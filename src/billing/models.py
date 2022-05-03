from tabnanny import verbose
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class BillingModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(
        _('Billing Title'), max_length=100, null=False, blank=True)

    subtitle = models.CharField(
        _('Billing SubTitle'), max_length=200)

    price = models.FloatField(
        _('Billing Price'), default=0.0, help_text="Membership Price")

    billing_expiry_days = models.IntegerField(
        default=30, help_text="Billing For x days..")

    description = models.TextField(
        _('Billing Description'), null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = _('Billing')
        verbose_name_plural = _('Billings')

    def __str__(self):
        return self.title + ' ' + self.price

    def get_price(self):
        price = '%s' % (self.price)
        return price

    def get_billing_days(self):
        return self.billing_expiry_days
