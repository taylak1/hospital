from django_filters import FilterSet
from .models import Doctor

class DoctorFilter(FilterSet):
    class Meta:
        model = Doctor
        fields = {
            'department': ['exact'],
            'specialty': ['exact'],
            'appointment_price': ['gt', 'lt']
        }