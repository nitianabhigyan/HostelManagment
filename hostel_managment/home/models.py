from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
# doc for phonenumber_field available on https://pypi.org/project/django-phonenumber-field/


#to be hidden from admin page even.
class password_db(models.Model):
	user_id = models.IntegerField(primary_key=True,null=False,validators=[MinValueValidator(10000),MaxValueValidator(2100107999)])
	password=models.CharField(null=False,max_length=160)
		
class student_db(models.Model):
	#primary_key.
	regn_no = models.IntegerField(primary_key=True,null=False,validators=[MinValueValidator(settings.MIN_REGN_NO),MaxValueValidator(2100107999)])
	student_name = models.CharField(null=False,max_length = 80)
	branch = models.CharField(null=False,max_length= 3)
	semester = models.PositiveSmallIntegerField(null=False)
	contact_no = PhoneNumberField(null=False)
	email_id = models.EmailField(unique=True)
	guardian_contact = PhoneNumberField(null=False)
	age = models.PositiveSmallIntegerField(null=False)
	#foreign key.                  # in case the student is removed or hostel is collapsed.
	hostel_name = models.ForeignKey("hostel_db",on_delete=models.SET_NULL,null=True,)
	photo = models.BinaryField()
	premanent_addr=models.TextField(null=False) 
	refund = models.IntegerField(default=0)
	room_no = models.CharField(null=True,max_length=4)
	def __unicode__(self):
		return str(self.regn_no)
	def __str__(self):
		return str(self.regn_no)
	class Meta:
		verbose_name="Student Detail"
		
class hostel_db(models.Model):
	# Primary key
	hostel_name=models.CharField(primary_key=True,max_length=20,choices = (settings.LIST_OF_HOSTELS))
	no_of_rooms = models.PositiveSmallIntegerField(null=False)
	caretaker_contact = PhoneNumberField(null= False)
	# Foreign key.
	warden_id = models.ForeignKey("warden_db",on_delete=models.SET_NULL,null= True,default=None)
	
	def __unicode__(self):
		return str(self.hostel_name)
	def __str__(self):
		return str(self.hostel_name)
	class Meta:
		verbose_name="Hostel Detail"
		
class warden_db(models.Model):
	#primary_key.
	warden_id = models.PositiveSmallIntegerField(primary_key=True, validators=[MinValueValidator(10000),MaxValueValidator(99999)])
	warden_name=models.CharField(null=False,blank=False,max_length=50)
	contact_no = PhoneNumberField(null=False)
	office_addr = models.TextField(max_length="200",null = False)
	email_id = models.EmailField(null=False,unique=True)
	chief_status = models.BooleanField(default = False)
	
	def __unicode__(self):
		return str(self.warden_id)
	def __str__(self):
		return str(self.warden_name)
	class Meta:
		verbose_name="Warden Detail"
"""
Class YourModel(models.Model):
    your_field = models.ForeignKey(YourOtherModel, db_constraint=False)
"""