from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator


class reset_pass_db(models.Model):
	regn_no = models.IntegerField(null=False,validators=[MinValueValidator(2011101000),MaxValueValidator(2100107999)])
	timestamp = models.DateTimeField()
	token0 = models.CharField(max_length=35,null = True)
	def __unicode__(self):
		return str(self.regn_no)
	def __str__(self):
		return str(self.regn_no)