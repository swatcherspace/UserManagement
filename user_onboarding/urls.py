from django.urls import path, include
# from .views import RenewalView, ClaimManagmentView, EndorsementManagmentView 
from .views import UserOnboardingViewSet, GetPortfolioViewSet, StockViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'user-onboard', UserOnboardingViewSet)
router.register(r'portfolio', GetPortfolioViewSet)
router.register(r'stock', StockViewSet)
from rest_framework.authtoken import views
    

app_name = 'user_onboarding'

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token)
]