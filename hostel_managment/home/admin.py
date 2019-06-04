from django.contrib import admin
from .models import student_db,hostel_db,warden_db,password_db

# Register your models here.
class studentadmin(admin.ModelAdmin):
	list_display = ('regn_no','student_name','semester','branch','refund')
	list_filter = ('branch','semester','refund')
	search_fields = ['regn_no','branch','semester','student_name']
class hosteladmin(admin.ModelAdmin):
	list_display = ('hostel_name','warden_id','no_of_rooms')

class wardenadmin(admin.ModelAdmin):
	list_display = ('warden_name','warden_id','chief_status')

	
admin.site.register(student_db,studentadmin)
admin.site.register(hostel_db,hosteladmin)
admin.site.register(warden_db,wardenadmin)