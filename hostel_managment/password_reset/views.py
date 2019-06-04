from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
from home.models import student_db
from home.password_writer import password_db_writer
from random import choice,randint
from .token_sender import mailer
from .models import reset_pass_db

result = None	
def index(request): 
# catch the hashed word
	global result
	if request.method == 'GET':
		operator = choice(['+','-','*'])
		num1 = randint(0,9)
		if operator == '-':
			num2 = randint(0,num1)
			result = num1 - num2
		elif operator == '+':
			num2 = randint(0,9)
			result = num1 + num2
		elif operator == '*':
			num2 = randint(0,9)
			result = num1 * num2

		question = str(num1) +" "+ str(operator) +" "+ str(num2) + " = "
		return render(request,'password_reset/reset.html',{'question':question,'flag':0})
	elif request.method == 'POST':
		# type conversion otherwise it won't be equal.
		if result == int(request.POST.get('answer')):
			stud_id = request.POST.get('stud_id')
			try:
				student_inst = student_db.objects.get(regn_no = stud_id)
				
			#except student_db.DoesNotExist:
			except:
				return HttpResponse("<h2>The entered student does not exist in our database.<br> Try signing up or contact admin </h2>")

			email = request.POST.get('usermail')
			student_no = request.POST.get('student_no')
			if student_no == student_inst.contact_no and email == student_inst.email_id:
				# call function to send mail with the the token as url
				# ADD A RANDOM SALT AND SAV IN DB
				token = str.split(make_password(stud_id),'p=')
				
				# create a database entry and save for an expiry for it.
				entry,created = reset_pass_db.objects.get_or_create(regn_no = student_inst.regn_no,timestamp = timezone.now(),token0=token[0])
				try:
					entry.save()
				except:
					return HttpResponse("<h2>Unable to process your request.<br> Please try again.</h2>")
				tomail = "pequal"+token[1]
				tomail = str.replace(tomail,"$","strdollar")
				tomail = str.replace(tomail,"+","strplus")
				tomail = str.replace(tomail,"/","strslash")
				
				mailer(student_inst.email_id,tomail)
				return HttpResponse("<h2> Kindly check your registered mail for Resetting link<br><strong>Note that it can take upto 15 minutes for the mail to reach.</h2>")
			else:
				return HttpResponse("<h2>The entered contact number or email does not matched with our database. <br> Try again or contact admin</h2>")
		else: 
			# generate a error message and tell to fill again
			return HttpResponse("<h2> Incorrect Captcha.</h2>")			
			
			
def token_verification(request,token1):
	token1 = str.replace(token1,"pequal","p=")
	token1 = str.replace(token1,"strdollar","$")
	token1 = str.replace(token1,"strplus","+")
	token1 = str.replace(token1,"strslash","/")

	if request.method == 'GET':
		# at any given time there SHUOLD BE LIMIT ON number if entries in database.
		#Message_me = Messages.objects.filter(username='myname', status=0).count()
		student_id = None
		entries = reset_pass_db.objects.all()
		for entry in entries:
			token = str(entry.token0)+str(token1)
			if check_password(entry,token):
				student_id = entry
				break
				
		if student_id == None:#ENTRY NOT FOUND TOKEN IS BOGUS.
			return HttpResponse("<h2>Invalid Token URL.<br>Please try again.</h2>")			
		else:
			entry = reset_pass_db.objects.filter(regn_no = str(student_id))
			entry.delete()
			request.session['stud_check'] = str(student_id)			
			return render(request,'password_reset/new_pass.html',{'flag':0})

def change(request):
	if request.method =='GET':
		return HttpResponse("<h2>Kindly Don't edit the URL.<br> This incident might be reported to the admin along with your IP.</h2>")
		
	elif request.method == 'POST':
		if request.session['stud_check'] == None:
			return HttpResponse("<h2>Your password could not be resetted</h2>")
		id = request.session['stud_check']
		id_entered  = request.POST.get('stud_id')
		if str(id) != str(id_entered):
			inst = reset_pass_db.objects.filter(regn_no=id)
			inst.delete()
			return HttpResponse("<h2>Your id verification failed<br> please try again<strong> all over again </strong>after some time.</h2>")
		else:
			password = request.POST.get('password')
			c_password = request.POST.get('confirm_password')
			if password != c_password:
				return render(request,'password_reset/new_pass.html',{'flag':1,'message':"<h2>The entered passswords do not match. <br> Please try again.</h2>"})
			else:
				inst = reset_pass_db.objects.filter(regn_no=id)
				inst.delete()
				if password_db_writer(id,password):
					request.session['stud_check'] = None
					# call for cleanup
					return HttpResponse("<h2>Your password was updated successfully.</h2>")
				else:
					return HttpResponse("<h2>Your password <strong>could not be </strong>updated .</h2>")
#verify the student name etc and change the password
	"""
	request_date = complaint.complaint_date
	current = datetime.datetime.now().date()
	diff = str(current - complaint_date)
	diff = int(diff[:2])
	# for days > 30 the month will auto inc to 30+ 
	if (diff > 15 and complaint.complaint_solved):
		# drop the row 
		#complaint.delete()
	"""