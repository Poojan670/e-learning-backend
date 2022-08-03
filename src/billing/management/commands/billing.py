from django.core.management.base import BaseCommand
from src.billing.models import BillingModel

# testing purposes!


class Command(BaseCommand):
    help = "Create Billing objects at startup"

    def handle(self, *args, **kwargs):
        if BillingModel.objects.count() == 0:
            BillingModel.objects.create(
                title="Annual Membership",
                subtitle="Unlimited access to all current & future Academind courses",
                price=199.0,
                billing_expiry_days=365,
                description='This is a recurring payment, charged automatically on a yearly basis. You can cancel anytime from inside your user profile to avoid being charged again once your billing cycle ends. For more information, please contact'
            )
            BillingModel.objects.create(
                title="Monthly Membership",
                subtitle="Best choice! Full flexibility and unlimited course access!",
                price=19.0,
                billing_expiry_days=30,
                description='This is a recurring payment, charged automatically on a monthly basis. You can cancel anytime from inside your user profile to avoid being charged again once your billing cycle ends. For more information, please contact'
            )
            self.stdout.write("Billing objects created successfully!")
        else:
            self.stdout.write("Billing objects already created!")
