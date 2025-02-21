from django.contrib.auth.models import AbstractUser
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

ROLE_CHOICES = (
	('Doctor', 'Doctor'),
	('Patient', 'Patient')
)
class UserProfile(AbstractUser):
	phone_number = PhoneNumberField(null=True, blank=True)
	profile_picture = models.FileField(upload_to='profile_pictures', null=True, blank=True)

	def  __str__(self):
		return f'{self.first_name} - {self.last_name}'

class Department(models.Model):
	department_name = models.CharField(max_length=32, unique=True)

	def __str__(self):
		return f'{self.department_name}'

class Specialty(models.Model):
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
	specialty_name = models.CharField(max_length=32, unique=True)

	def __str__(self):
		return f'{self.department} - {self.specialty_name}'

class Doctor(UserProfile):
	role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='Doctor')
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
	shift_start = models.TimeField()
	shift_end = models.TimeField()
	DAYS_CHOICES = (
		('Mon', 'Mon'),
		('Tue', 'Tue'),
		('Wed', 'Wed'),
		('Thu', 'Thu'),
		('Fri', 'Fri'),
		('Sat', 'Sat'),
	)
	working_days = MultiSelectField(choices=DAYS_CHOICES, max_choices=6, max_length=128)
	appointment_price = models.PositiveSmallIntegerField()
	GENDER_CHOICES = (
		('Man', 'Man'),
		('Woman', 'Woman')
	)
	gender = models.CharField(choices=GENDER_CHOICES, max_length=16, null=True, blank=True)
	experience = models.PositiveSmallIntegerField(null=True, blank=True)

	def  __str__(self):
		return f'{self.first_name} {self.last_name}, {self.department} - {self.specialty}'

	class Meta:
		verbose_name_plural = 'Doctors'

class Patient(UserProfile):
	role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='Patient')
	emergency_contact = PhoneNumberField(null=True, blank=True)
	blood_type = models.CharField(max_length=64)

	def  __str__(self):
		return f'{self.first_name} - {self.last_name}'

	class Meta:
		verbose_name_plural = 'Patients'

class Appointment(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	date_time = models.DateTimeField()
	STATUS_CHOICES = (
		('Planned', 'Planned'),
		('Completed', 'Completed'),
		('Canceled', 'Canceled')
	)
	status = models.CharField(max_length=32, choices=STATUS_CHOICES)

	def  __str__(self):
		return f'{self.patient} - {self.doctor}'

class MedicalRecord(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	diagnosis = models.CharField(max_length=128)
	treatment = models.CharField(max_length=64)
	prescribed_medication = models.CharField(max_length=128)
	created_at = models.DateTimeField()

	def  __str__(self):
		return f'{self.patient} - {self.doctor}'

class Feedback(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
	comment = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def  __str__(self):
		return f'{self.patient} - {self.doctor} , {self.rating}'

	def clean(self):
		super().clean()
		if not self.rating and not self.comment:
			raise ValidationError('Choose minimum one of (rating, comment)!')

class Chat(models.Model):
	users = models.ManyToManyField(UserProfile)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return f'{self.users}'

class Massage(models.Model):
	author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
	text = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='massage_images', null=True, blank=True)
	video = models.FileField(upload_to='massage_videos', null=True, blank=True)
	created_date = models.DateTimeField(auto_now_add=True)
