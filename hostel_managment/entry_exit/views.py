from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Student_Still_Out,Guard_Detail
from django.utils import timezone # using this instead of datetime.datetime to prevent timezone related error
from student.models import student_db
from student.views import img_proc
from django.contrib.auth.hashers import check_password
from django.core import serializers


def index(request):
	if request.method == 'GET' and not request.is_ajax():
		if request.session.get('Guard_ID_Selected') != None:
			# implement a verification method
			dbobj = Student_Still_Out.objects.all()
			return render(request,'entry_exit/logged_in_page.html',{'alert_flag':0,'db_object':dbobj})
		else: 
			return redirect('/entry')
	#for new submissions in Temp_db(Student_Still_Out table)
	elif request.method == 'POST':
		if request.session.get('Guard_ID_Selected') != None:
			entered_regn_no = request.POST['Regn_No']
			student_db_inst = None # initialising the variable for use throughout the section(Not just in try block)
			# this piece is redundant.
			try:
				student_db_inst = student_db.objects.get(regn_no=entered_regn_no)
			except student_db.DoesNotExist:
				message = "The Entered Registration Number does not exist in the database.<br>Please contact admin."
				return render(request,'entry_exit/logged_in_page.html',{'alert_flag':1,'alert_message':message})
				
			if Student_Still_Out.objects.filter(regn_no = entered_regn_no).exists():
				student_inst = Student_Still_Out.objects.get(regn_no=entered_regn_no)
				student_inst.in_date = timezone.now()
				student_inst.is_completed = True
		
				try:
					student_inst.save()
				except: #if the instance could not be updated then:-
					return HttpResponse("Could not update the entry.<br>Please try again")
					
				message = "Entry Updated for Registration Number: "+str(student_inst.regn_no)+"\\nReason of visit: "+str(student_inst.reason)
				dbobj = Student_Still_Out.objects.all()
				return render(request,'entry_exit/logged_in_page.html',{'alert_flag':1,'alert_message':message,'db_object':dbobj})
			else:
				entered_reason = request.POST['Reason']
				student_inst = None	
				try:
					student_inst = Student_Still_Out(regn_no=student_db_inst,is_completed=False,reason=entered_reason)
					student_inst.save()
				except:
					return HttpResponse("Unable to save your entry for previous entry.<br>Please try again later.")
				message = "Entry for Regn_No: "+str(student_inst.regn_no)+" Submitted Successfully. Your id is "+str(student_inst.entry_id)
				dbobj = Student_Still_Out.objects.all()
				return render(request,'entry_exit/logged_in_page.html',{'alert_flag':1,'alert_message':message,'db_object':dbobj})
		else:
			return redirect('/entry')
			
def ajax_handler(request):
	if request.is_ajax():
		if request.session.get('Guard_ID_Selected') != None:
			# verifying if the student exists in the database
			entered_regn_no = request.GET['Regn_No_ajax']
			try:
				student_db_inst = student_db.objects.get(regn_no=entered_regn_no)
			except student_db.DoesNotExist:
				return JsonResponse({'flag':1,'error_message':'Entered student does not exist in our system.\n Please signup or contact admin'})
			
			if Student_Still_Out.objects.filter(regn_no = entered_regn_no).exists():
				flag = 1
				#if flag ==1 is returned it means: the student is out
			else:
				flag = 0
			student_data={'name':student_db_inst.student_name,'regn_no':student_db_inst.regn_no,'branch':student_db_inst.branch,'contact_no':str(student_db_inst.contact_no),'hostel':str(student_db_inst.hostel_name)}
			
			data ={'flag': flag,'student':student_data}
			img_proc(student_db_inst)
			return JsonResponse(data)
		else:
			return redirect('/entry')
	
def login(request):
	if request.method=='GET':
		return render(request,'entry_exit/login_page.html',{'flag':0,})
	
	elif request.method == 'POST':
		id = request.POST['userid']
		try:
			Guard_inst = Guard_Detail.objects.get(Employee_Id = id)
		except Guard_Detail.DoesNotExist:
			return render(request,'entry_exit/login_page.html',{'flag':1,'message':"Wrong ID please try again or contact admin."})
		
		password_entered = request.POST['password']
		if check_password(password_entered,Guard_inst.Password):
			request.session['Guard_ID_Selected'] = Guard_inst.Employee_Id
			return redirect('/entry/guard')
		else:
			return render(request,'entry_exit/login_page.html',{'flag':1,'message':"Wrong Password please Try again"})
		
def logout(request):
	request.session['Guard_ID_Selected'] = None
	return redirect('/entry')