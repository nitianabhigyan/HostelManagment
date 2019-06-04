from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import password_db,student_db,hostel_db
from .password_writer import password_db_writer
from django.contrib.auth.hashers import check_password
from PIL import Image


#Add logic to automatically add +91 to the number instead of asking the user.
#Add server side form verification bcz html can be cracked by using inspect.
def index(request):
	return render(request,'home/home_page.html',{'flag':0})
	
# can be included in index as if request.method == 'POST'	
def password_check(request):
	if request.method == 'POST':
		id = request.POST.get('userid')
		try :
			stud_inst = student_db.objects.get(regn_no=id)
		except student_db.DoesNotExist:
			return HttpResponse("<h2>The entered roll no does not exist.<br> try signing up.</h2>")
			
		password_entered = request.POST.get('password')
		try:
			id_instatnce = password_db.objects.get(user_id=id)
			if check_password(password_entered,id_instatnce.password):
			# need to verify if student or warden.
				request.session['selected_student_id'] = id
				#request.session.set_expiry(0)
				return redirect('/home/student/')
			else: 
				return render(request,'home/home_page.html',{'flag':1,'message':"Wrong password try again."})
				# return HttpResponse("<h2>Wrong password try again.</h2>")
			# if the entered id is not found by try block.
		except password_db.DoesNotExist:
			return render(request,'home/home_page.html',{'flag':1,'message':"Wrong ID please try again."})
			# return HttpResponse("<h2>Not found the form details please try again.</h2>")	
	else:
		return HttpResponse("<h2>Invalid request please try again</h2>")

def signup(request):
	if request.method =='GET':
		return render(request,'home/sign_up.html')
		
	elif request.method =='POST':
		# data extraction from populated form.
		name =request.POST.get('name')
		id = request.POST.get('regn_no')
		# Check if entry already exist.
		
		try:# if the student is already present in the database
			student_inst = student_db.objects.get(regn_no=id)
			return HttpResponse("<h2>The entry for this registration number already exists.<br>Contact admin for more information.</h2>")
			
		except student_db.DoesNotExist:
			password = request.POST.get('password')
			c_password = request.POST.get('confirm_password')
			if str(password) != str(c_password):
				return HttpResponse("<h2>The entered password do not match</h2>")
			else:
					name = request.POST.get('name')
					branch_entered = request.POST.get('branch')
					email = request.POST.get('usermail')
					hostel = request.POST.get('hostel')
					student_no = request.POST.get('student_no')
					semester_entered = request.POST.get('semester')
					age_entered = request.POST.get('age')
					guardian_no = request.POST.get('guardian_no')
					#resizing the image for security and reducing storage.
					photo = Image.open(request.FILES['photo'])
					size = (350,350)
					photo = photo.resize(size,Image.ANTIALIAS)
					bdata=photo.tobytes()
					address = request.POST.get('address')
					
					try:# ALSO IF STUD EXISTS U WILL RECREATE
						#if the PASSWORD OF user was ALREADY CREATED (say the admin deleterd the entry)
						pass_inst = password_db.objects.get(user_id=id)
						pass_inst.delete()
					except password_db.DoesNotExist:
						# try:
						stud_inst = student_db(regn_no=id,student_name=name,branch = branch_entered,semester=semester_entered,contact_no = student_no,email_id = email,guardian_contact = guardian_no,age = age_entered,hostel_name= hostel_db.objects.get(hostel_name=hostel),photo=bdata,premanent_addr = address)
						stud_inst.save()

						if password_db_writer(id,password):
							
							return HttpResponse("<h2>Id created successfully. go back to home page</h2>")
						else:
							instance_Student = student_db.objects.get(regn_no=id)
							instance_Student.delete()
							return HttpResponse("<h2> Password creation unsucessfull .<br> Please try again. </h2>")
						#Hostel does not exist or any other problem.
						# except:
							# return HttpResponse("<h2> The Id was not created.<br>Try again or contact admin.</h2>")
					
	return HttpResponse("<h2>Form submitted.</h2>")
