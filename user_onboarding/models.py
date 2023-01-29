from datetime import datetime
# Create your models here.
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

# Token Generation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class User(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    email_id = models.EmailField(verbose_name='email address',
        max_length=255,
        unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    created = models.DateTimeField(default=datetime.now(tz=timezone.utc), blank=True)
    modified = models.DateTimeField(auto_now_add=True, blank=True)

class UserPortfolio(models.Model):
    stock_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_portfolio")
    name = models.CharField(max_length=75, null=True, blank=True)
    created = models.DateTimeField(default=datetime.now(tz=timezone.utc), blank=True)
    modified = models.DateTimeField(auto_now_add=True, blank=True)


#Data for portfolio mgmt
# class Portfolio(models.Model):
#     # user_id = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=75, null=True, blank=True)
#     shares_outstanding = models.IntegerField(null= True, blank=True)
#     dividend_rate = models.FloatField(null=True, blank=True)
#     debt_to_equity = models.FloatField(null=True, blank=True)
#     book_value_per_share = models.FloatField(null=True, blank=True)
#     roe = models.FloatField(null=True, blank=True)
#     current_ratio = models.FloatField(null=True, blank=True)
#     pe_ratio = models.FloatField(null=True, blank=True)
#     pb_ratio = models.FloatField(null=True, blank=True)#Price to Book Value
#     market_cap = models.FloatField(null=True, blank=True)
#     earning_per_share = models.FloatField(null=True, blank=True)
#     industry_pe = models.FloatField(null=True, blank=True)
#     capped_type = models.CharField(max_length=75, null=True, blank=True)
#     dividend_yield_percent = models.FloatField(null=True, blank=True)
#     face_value = models.FloatField(null=True, blank=True)
#     news = models.CharField(max_length=75, null=True, blank=True)
#     created = models.DateTimeField(default=datetime.now, blank=True)
#     modified = models.DateTimeField(auto_now_add=True, blank=True)
    