
from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')
        str_fields = request.GET.get('fields', '') if request else None
        fields = str_fields.split(',') if str_fields else None
        super(UserSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = User
        fields = '__all__'
class UserPortfolioSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')
        str_fields = request.GET.get('fields', '') if request else None
        fields = str_fields.split(',') if str_fields else None
        super(UserPortfolioSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = UserPortfolio
        fields = '__all__'
# class PortfolioSerializer(serializers.ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         request = kwargs.get('context', {}).get('request')
#         str_fields = request.GET.get('fields', '') if request else None
#         fields = str_fields.split(',') if str_fields else None
#         super(PortfolioSerializer, self).__init__(*args, **kwargs)
#         if fields is not None:
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)

#     class Meta:
#         model = Portfolio
#         fields = '__all__'