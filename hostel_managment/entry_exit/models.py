from django.core.validators import MaxValueValidator
from django.db import models
from home.models import student_db
from django.db.models.signals import post_save,pre_save # added
from .signals import DB_Save_Detect,Guard_Password_Manager

class Entry_Exit(models.Model):
	entry_id = models.AutoField(primary_key=True,)
	regn_no = models.ForeignKey(student_db,on_delete=models.CASCADE)
	out_date = models.DateTimeField(null=False)
	in_date = models.DateTimeField(null=False)
	reason = models.CharField(max_length=200,null = False)

	def __str__(self):
		return str(self.entry_id)
	class Meta:
		verbose_name="Entry Exit Detail"
	
class Guard_Detail(models.Model):
	Employee_Id = models.IntegerField(primary_key=True,null=False)
	Guard_Name = models.CharField(null=False,max_length = 80)
	Contact_No = models.IntegerField(null=False,validators=[MaxValueValidator(9999999999)])
	Password = models.CharField(null=False,max_length=160)
	Confirm_Password = models.CharField(null=True,max_length=160,default=None)
	
	def __str__(self):
		return str(self.Employee_Id)
		
	class Meta:
		verbose_name = "Guard Detail"
		verbose_name_plural = "Guards Details"
	
pre_save.connect(Guard_Password_Manager,sender=Guard_Detail)
		
class Student_Still_Out(models.Model):
	entry_id = models.AutoField(primary_key=True,)
	regn_no = models.ForeignKey(student_db,on_delete=models.CASCADE)
	is_completed = models.BooleanField(default=False)
	out_date = models.DateTimeField(auto_now_add=True,editable=True,null=False)
	in_date = models.DateTimeField(null=True,default=None)
	reason = models.CharField(max_length=200,null = False)

	def __str__(self):
		return str(self.entry_id)
	
	class Meta:
		verbose_name= "Student Outside Campus"
		verbose_name_plural = "Students Outside Campus"
post_save.connect(DB_Save_Detect,sender=Student_Still_Out)