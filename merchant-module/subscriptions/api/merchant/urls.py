from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'package', views.MerchantPackageAPI)
router.register(r'subscribe', views.MerchantSubscribeAPI)
router.register(r'subscription', views.MerchantSubscriptionHistoryAPI)
urlpatterns = [

]
urlpatterns += router.urls
