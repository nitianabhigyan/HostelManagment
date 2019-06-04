from django.shortcuts import render,redirect
from .models import complaints_db,application_db
from home.models import student_db, hostel_db, password_db
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from PIL import Image
from time import sleep
from os import remove
from threading import Thread
import datetime

def index(request):
	id = request.session.get('selected_student_id')
	if id == None: #if user is logged out
		return redirect("/")
	else:
		student_inst= student_db.objects.get(regn_no = id)
		complaints = complaints_collect(id)
		img_proc(student_inst)
		return render(request,'student/student_loggedin.html',{'student':student_inst,'alert':0,'message':"",'complaints':complaints})

#intermediate functions to reduce main index() and new_complaint func
def img_proc(student_inst):
	bdata= student_inst.photo
	size = (350,350)
	#works without raw mode.
	imagestu=Image.frombytes('RGB',size,bdata)
	img_name = "student/static/student/"+str(student_inst.regn_no) + ".jpg"
	imagestu.save(img_name)
	warden = hostel_db.objects.get(hostel_name = student_inst.hostel_name).warden_id
	#Create a temp jpg & call delete func and del the img after 5 sec.
	t1 = Thread(target = img_delete, args= (img_name,))
	t1.start()

def img_delete(img_name):
	sleep(4)
	remove(img_name)
	
def complaints_collect(id):
	if complaints_db.objects.filter(regn_no = id).exists():
		results = complaints_db.objects.filter(regn_no = id)
	else:
		results = None
	return results
	
def new_complaint(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		type = request.POST.get('Type')
		try:
			#found photo
			photo = Image.open(request.FILES['photo'])
			size = (350,350)
			photo_processed = photo.resize(size,Image.ANTIALIAS)
			bdata=photo_processed.tobytes()
		except:
			bdata = None
		
		desc = request.POST.get('description')
		id = request.session.get('selected_student_id')
		student_inst= student_db.objects.get(regn_no = id)
		complaints = complaints_collect(id)
		try:
			complaint_inst = complaints_db(regn_no = student_inst,complaint_title = title,complaint_type= type,complaint_date = datetime.datetime.now(),complaint_image= bdata,)
			complaint_inst.save()
			flag = 1
		except:
			flag = 0
		if flag:
			img_proc(student_inst)
			return render(request,'student/student_loggedin.html',{'student':student_inst,'alert':1,'message':"The complaint was submitted successfully",'complaints':complaints})
		else :
			img_proc(student_inst)
			return render(request,'student/student_loggedin.html',{'student':student_inst,'alert':1,'message':"The complaint was submitted successfully",'complaints':complaints})

# Automatically sends mailed notification on being accepted or declined (using Magic!)
#Automatically deletes declined entries (fir details look into ./signals.py)
def application(request):
	if request.method == "GET":
		return render(request,"student/leave_form.html",{'flag':0})
	elif request.method == "POST":
		id = request.session.get('selected_student_id')
		if id == None:
			return redirect("/")
		password_entered = request.POST.get('password')
		id_instatnce = password_db.objects.get(user_id=id)
		if check_password(password_entered,id_instatnce.password):
			# converting from stringto datetime obj
			start = request.POST.get("start_date")
			start = datetime.datetime.strptime(start,'%Y-%m-%d')
			current = datetime.datetime.now().date().strftime('%Y-%m-%d') #till .date() dt obj after that returns str now
			current = datetime.datetime.strptime(current,'%Y-%m-%d')# returns dt obj
			end = request.POST.get("end_date")
			end = datetime.datetime.strptime(end,'%Y-%m-%d')
	#date verification from form
			if start > current and end > current:
				if end >= start:
					if application_db.objects.filter(reg_no=id,start_date = start).exists():
						return render(request,"student/leave_form.html",{'flag':1,'message':"An entry for the same day already exists. Kindly wait or contact admin."})
					else:
						reason_entered = request.POST.get("reason")
						# to satisfy foreign key criteria
						try:
							inst = application_db(reg_no=student_db.objects.get(regn_no=id),reason= reason_entered,start_date=start,end_date=end)
							inst.save()
						except:
							return render(request,"student/leave_form.html",{'flag':1,'message':"Entry could not be made Please contact admin"})
						#print(request.session.get_expiry_age())
						return redirect("/home/student")
				else:
					return render(request,"student/leave_form.html",{'flag':1,'message':"End Date should be greater than OR equal start Date!"})
			else:
				return render(request,"student/leave_form.html",{'flag':1,'message':"Entered Dates should be greater than present Date!"})
			
		else:
			return render(request,"student/leave_form.html",{'flag':1,'message':"wrong password entered"})

#script to delete very old and solved complaint.
def complaint_check(id):
	complaints = complaints_collect(id)
	if (complaints != None):
		for complaint in complaints:
			complaint_date = complaint.complaint_date
			current = datetime.datetime.now().date()
			diff = str(current - complaint_date)
			diff = int(diff[:2])
			# for days > 30 the month will auto inc to 30+ 
			if (diff > 14 and complaint.complaint_solved):
				# drop the row 
				complaint.delete()
				
def alter_student(request):
		id = request.session.get('selected_student_id')
		if id == None: #if user is logged out
				return redirect("/")
		else:
			student_inst = student_db.objects.get(regn_no = id)
			if request.method == "GET":
				return render(request,'student/alter_form.html',{'student':student_inst,'flag':0,'message':""})
			elif request.method == "POST":
				password_entered = request.POST.get('password')
				id_instatnce = password_db.objects.get(user_id=id)
				if check_password(password_entered,id_instatnce.password):
					#maybe add a verification layer.
					student_inst.student_name = request.POST.get('name')
					student_inst.email_id = request.POST.get('email')
					student_inst.contact_no = request.POST.get('student_no')
					hostel = request.POST.get('hostel')
					student_inst.hostel_name = hostel_db.objects.get(hostel_name =hostel)
					student_inst.semester = request.POST.get('semester')
					try:
						student_inst.save()
						return logout(request)
					except:
						return render(request,'student/alter_form.html',{'student':student_inst,'flag':1,'message':"Database could not be updated. Please try again or contact admin"})
				else:
					return render(request,'student/alter_form.html',{'student':student_inst,'flag':1,'message':"Wrong password. Please try again"})
			
def logout(request):
	t1 = Thread(target = complaint_check, args= (request.session.get('selected_student_id'),))
	t1.start()
	request.session['selected_student_id'] = None
	return redirect("/")