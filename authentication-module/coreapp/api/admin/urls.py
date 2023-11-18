from rest_framework import routers
from django.urls import path
from coreapp.api.admin import views

router = routers.DefaultRouter()
router.register(r'country', views.CountryAdminAPI)
router.register(r'module', views.ModuleAdminAPI)
router.register(r'modulepermission', views.ModulePermissionAdminAPI)
router.register(r'permissiongroup', views.PermissionGroupAdminAPI)
router.register(r'userpermission', views.UserPermissionAdminAPI)

urlpatterns = [
    path('loginhistory/', views.LoginHistoryAdminAPI.as_view()),
]

urlpatterns += router.urls
