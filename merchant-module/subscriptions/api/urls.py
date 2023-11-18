from django.urls import path, include

urlpatterns = [
    path('admin/', include('subscriptions.api.admin.urls')),
    path('merchant/', include('subscriptions.api.merchant.urls')),
]
