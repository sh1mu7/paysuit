from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'business', views.MerchantBusinessAPI)
router.register(r'businessdocument', views.MerchantBusinessDocumentAPI)

urlpatterns = [

]
urlpatterns += router.urls
