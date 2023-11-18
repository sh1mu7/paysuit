from django.urls import path, include

app_name = 'api-v1'

urlpatterns = [
    path('merchant/', include('coreapp.api.urls')),
    path('subscription/', include('subscriptions.api.urls')),
]
