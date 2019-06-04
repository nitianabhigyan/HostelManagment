from .models import password_db
from django.contrib.auth.hashers import make_password


def password_db_writer(id,password):
		try:
			hashed_password = make_password(password)
			my_inst = password_db(user_id = id,password= hashed_password)
			my_inst.save()
			return True
		except:
			return False