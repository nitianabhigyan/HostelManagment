from threading import Thread
from entry_exit import models
from django.contrib.auth.hashers import make_password

def DB_Save_Detect(sender,instance,**kwargs):
	if sender == models.Student_Still_Out:
		if instance.is_completed:
			t = Thread(target=DB_Transfer,args=(instance,))
			t.start()

def DB_Transfer(instance):
	if instance.is_completed:
		t_in_date = instance.in_date
		t_out_date = instance.out_date
		t_regn_no = instance.regn_no
		t_reason = instance.reason
		Final_inst = models.Entry_Exit(regn_no=t_regn_no,out_date=t_out_date,in_date=t_in_date,reason=t_reason)
		Final_inst.save()
		instance.delete()
		
def Guard_Password_Manager(sender,instance,**kwargs):
	if sender == models.Guard_Detail:
		if instance.Password == instance.Confirm_Password:
			hashed_password = make_password(str(instance.Password))
			instance.Password= hashed_password
			instance.Confirm_Password = None
			#instance.save()
			# no need to call save as it was already called and that is why we are heres
		else:
			raise ValueError("The entered passwords do not match please try again")