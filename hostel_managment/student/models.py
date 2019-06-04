from django.db import models
from home.models import student_db
from .signals import save_mail# added
from django.db.models.signals import post_save # added

# Create your models here.
class complaints_db(models.Model):
	complaint_id = models.AutoField(primary_key=True,)
	regn_no = models.ForeignKey(student_db,on_delete=models.CASCADE)
	complaint_title = models.CharField(max_length = 50,null = False)
	complaint_type = models.CharField(max_length = 11,null = False)
	complaint_date = models.DateField()
	complaint_image = models.BinaryField(null = True)
	complaint_solved = models.BooleanField(default=False)

	def __str__(self):
		return str(self.complaint_title)
	class Meta:
		verbose_name = "Complaint "
		verbose_name_plural = "Complaints Managment"
		
class application_db(models.Model):
	app_id = models.AutoField(primary_key=True)
	reg_no = models.ForeignKey(student_db,on_delete=models.CASCADE)
	reason = models.CharField(max_length=251,null = False)
	start_date = models.DateField() # end date > start date
	end_date = models.DateField()
	accepted = models.BooleanField(default = False)
	declined = models.BooleanField(default = False)
	
	def __unicode__(self):
		return str(self.reg_no)
	def __str__(self):
		return str(self.reg_no)

	class Meta:
		verbose_name = "Application"
		verbose_name_plural = "Applications Managment"
post_save.connect(save_mail,sender=application_db)