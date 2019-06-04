import os
import tkinter as TK
from threading import Thread

top = TK.Tk()

def Threader(to_Start,_args):
	t1 = Thread(target=to_Start)
	t1.start()
	
def Default_server_start():

	os.system("cmd")
   
def End_Server():
	#os.system("")
	print("entered end_server")

Basic_Button = TK.Button(top, text ="Start Localhost Server", command = Threader(Default_server_start,None))
End_Button = TK.Button(top,text="Stop the Server",command=End_Server)

Basic_Button.pack()
End_Button.pack()
top.mainloop()