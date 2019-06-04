from django.contrib.auth.hashers import check_password
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
import smtplib

def mailer(reciever,token):
	
	mail = smtplib.SMTP('smtp.gmail.com',587)
	mail.starttls()
	mail.ehlo()
	# change this
	mail.login(settings.MAIL_ID,settings.MAIL_PASS)
	message=MIMEMultipart('alternative')
	sender = settings.MAIL_ID
	message['From'] = "Hostel Managment System"
	message['To'] = reciever
	message['Subject']="Password Reset Request"
	
	mess = "Hello User, \n Looks like you have had some trouble in logging with us. No worries, this email has been generated to help you just with that. \n Click on the link below to reset your password. \n " +str(settings.WEB_URL)+"reset/"+str(token)+ "\n\n If that doesnt works try copying and pasting this in your browser while being connected to college WiFi:- \n "+str(settings.WEB_URL)+"reset/" + str(token) 
	
	# for sending through file system read
	message.attach(MIMEText(mess,'plain'))
	mail.sendmail(sender,reciever, message.as_string())
	mail.quit()	