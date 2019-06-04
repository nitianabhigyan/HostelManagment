from django.contrib import admin
from .models import Student_Still_Out,Entry_Exit,Guard_Detail


class Student_Still_Outadmin(admin.ModelAdmin):
	list_display = ('regn_no','entry_id','in_date','out_date')
	list_filter = ('out_date',)

class Entry_Exitadmin(admin.ModelAdmin):
	list_display = ('regn_no','in_date','out_date','reason')
	list_filter = ('regn_no','in_date','out_date')
	date_hierarchy = 'in_date'
	search_fields = ('regn_no__regn_no','reason') # since reg_no is a foreign key therefore nameoffield__nameoffieldinfktable

class Guard_Detailadmin(admin.ModelAdmin):
	list_display = ('Employee_Id','Guard_Name','Contact_No')

	
admin.site.register(Student_Still_Out,Student_Still_Outadmin)
admin.site.register(Entry_Exit,Entry_Exitadmin)
admin.site.register(Guard_Detail,Guard_Detailadmin)