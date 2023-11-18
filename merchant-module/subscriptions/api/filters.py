from django_filters import rest_framework as dj_filters

from subscriptions.models import Package


class PackageFilter(dj_filters.FilterSet):
    name = dj_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Package
        fields = ('name', 'is_active')
