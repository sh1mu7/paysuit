from django.urls import path, include

urlpatterns = [
    path('admin/', include('coreapp.api.admin.urls')),
    path('merchant/', include('coreapp.api.merchant.urls'))
]
