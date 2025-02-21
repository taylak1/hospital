from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class DoctorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'department', 'specialty', 'working_days',
                  'experience', 'gender', 'shift_start', 'shift_end', 'appointment_price')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Doctor.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class DoctorLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class PatientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'emergency_contact', 'blood_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Patient.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class PatientLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']

class DepartmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name',]

class SpecialtyListSerializer(serializers.ModelSerializer):
    department = DepartmentDetailSerializer()

    class Meta:
        model = Specialty
        fields = ['id', 'specialty_name', 'department']

class SpecialtyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['specialty_name']

class DoctorListSerializer(serializers.ModelSerializer):
    department = DepartmentDetailSerializer()

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'department', 'experience']

class DoctorDetailSerializer(serializers.ModelSerializer):
    department = DepartmentDetailSerializer()
    specialty = SpecialtyDetailSerializer()

    class Meta:
        model = Doctor
        fields = ['profile_picture', 'first_name', 'last_name', 'gender',
                  'experience', 'department', 'specialty', 'shift_start',
                  'shift_end', 'working_days', 'appointment_price', 'phone_number']

class DoctorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'profile_picture', 'first_name', 'last_name',
                  'phone_number', 'emergency_contact', 'blood_type']

class PatientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSimpleSerializer()
    doctor = DoctorSimpleSerializer()
    date_time = serializers.DateTimeField(format('%Y-%B-%d  %H:%M'))

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'status', 'date_time']

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSimpleSerializer()
    doctor = DoctorSimpleSerializer()
    created_at = serializers.DateTimeField(format='%Y-%B-%d  %H:%M')

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'treatment',
                  'prescribed_medication', 'created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    patient = PatientSimpleSerializer()
    doctor = DoctorSimpleSerializer()

    class Meta:
        model = Feedback
        fields = ['id', 'patient', 'doctor', 'rating', 'comment', 'created_at']

