import urllib.request
from time import sleep
import telegram
#import telegram_shell_UploadDownload as UpDownfunctions
from telegram import ParseMode
import os
import json
import sys
import re
import glob


def cd_function(folder, chat_id, ScriptLocationPath):
    try:
        f=open(ScriptLocationPath+"/"+str(chat_id)+"_telegram-shell-status.json", "r")  #Check if this chat has a previous location
        data = json.load(f)
        currentLocation = data['PATH']
        f.close()
    except:
        currentLocation = "/home"
    
    folder= currentLocation +"/" +folder
    try:  #Check if next location exist
        os.chdir(folder)
        currentLocation=os.getcwd()
        f=open(ScriptLocationPath+"/"+str(chat_id)+"_telegram-shell-status.json", "w+")
        text = """{
            "PATH":"""+'"'+currentLocation+'"'"""
        }"""
        f.write(text)
        f.close()  
        resp = "PATH: $"+currentLocation+"\n\n\n"+os.popen("ls").read()
        return resp
        #send_message(resp,chat_id) 
    except FileNotFoundError:
        resp = "File not found, please check again"
        return resp
        #send_message(resp,chat_id) 

def ls_function(chat_id, ScriptLocationPath):
    try:
        f=open(ScriptLocationPath+"/"+str(chat_id)+"_telegram-shell-status.json", "r")  #Check if this chat has a previous location
        data = json.load(f)
        currentLocation = data['PATH']
        f.close()
    except:
        currentLocation = "/home"
    os.chdir(currentLocation)
    resp = "PATH: $"+currentLocation+"\n\n\n"+os.popen("ls").read()
    return resp 
    
def get_ip():
 return urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
