from threading import Thread
import student

def save_mail(sender,instance,**kwargs):
	"""
	RUNS IN SEP. THREAD Result : NO
	""" 
	if sender == student.models.application_db:
		if instance.accepted and instance.declined:
			instance.accepted = False
			instance.declined = False
			instance.save()
			#My first custom error :).
			raise ValueError("You can't set 'accept' and 'declined' true at same time.\n This is not possible.\n The entry is saved without being accepted or rejected.")
		else:
			t1 = Thread(target = Mailer, args= (instance,))
			t1.start()
			
def Mailer(instance):
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from django.conf import settings
	from smtplib import SMTP

	
	mail = SMTP('smtp.gmail.com',587)
	mail.starttls()
	mail.ehlo()

	reciever = instance.reg_no.email_id
	mail.login(settings.MAIL_ID,settings.MAIL_PASS)
	message=MIMEMultipart('alternative')
	sender = settings.MAIL_ID
	message['From'] = "Hostel Managment System"
	message['To'] = reciever
	message['Subject']="Notification For leave application"
	mess = "Dear "+str(instance.reg_no.student_name)+",\n\n" 
	
	if instance.accepted:
		mess += "We are happy to inform you that your request for leave starting on " +str(instance.start_date)+" to "+str(instance.end_date)+" has been accepted  by the hostel incharge.\n As a result you will be entitled for a refund in mess money for the stated dates.\nThank you, for your time.\n If you have any further queries please feel free to contact the administrator.\n\n\n Greetings,\n Hostel Managment Team\n"
		
	elif instance.declined:
		mess += "We regret to inform you that your request for leave (and henceforth mess refund) starting on " +str(instance.start_date)+" to "+str(instance.end_date)+" has been declined by the hostel incharge\nAs a result you will 'NOT' be entitled for a refund in mess money for the stated dates.\n If you have any further queries please feel free to contact the administrator.\n\n\n Greetings,\n Hostel Managment Team\n"
		instance.delete()
	elif (instance.accepted == False) and (instance.declined==False):
		mess+="A request for your leave starting on " +str(instance.start_date)+" to "+str(instance.end_date)+"has been recieved. \n Kindly keep patience while it is being reviewed.\nIf you have any further queries kindly contact hostel warden or admin.\n\n\n Greetings,\n Hostel Managment Team\n"
	message.attach(MIMEText(mess,'plain'))
	mail.sendmail(sender,reciever, message.as_string())
	mail.quit()	

