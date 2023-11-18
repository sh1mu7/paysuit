from django_filters import rest_framework as dj_filters

from ..models import Country, LoginHistory


class CountryFilter(dj_filters.FilterSet):
    name = dj_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Country
        fields = ('name', 'is_active')


class LoginHistoryFilter(dj_filters.FilterSet):
    user = dj_filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    ip_address = dj_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = LoginHistory
        fields = ('user', 'ip_address')
