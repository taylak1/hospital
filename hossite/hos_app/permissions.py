from rest_framework import permissions

class CheckDoctor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.role == 'Doctor'

class CheckPatient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.role == 'Patient'

