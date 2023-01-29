from django.contrib import admin

# Register your models here.
from .models import *


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email_id', 'is_active', 'staff', 'admin',
                    'created',
                    'modified')


admin.site.register(User, UserModelAdmin)
