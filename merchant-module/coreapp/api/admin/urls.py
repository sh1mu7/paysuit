from rest_framework import routers
from django.urls import path
from coreapp.api.admin import views

router = routers.DefaultRouter()
router.register(r'businesscategory', views.AdminBusinessCategoryAPI)
router.register(r'business', views.AdminBusinessAPI)
router.register(r'businessdocument', views.AdminBusinessDocumentAPI)

urlpatterns = [

]

urlpatterns += router.urls
