import os

def run(**args):

	print ("[*] In dirlistener module")
	files = os.listdir(".")
	
	return str(files)
