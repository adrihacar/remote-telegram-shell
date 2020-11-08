import urllib.request
import requests
from time import sleep
import telegram
import telegram_shell_functions.telegram_shell_Basicfunctions as Basicfunctions
from telegram import ParseMode
import os
import json
import sys
import re
import glob


def downloadFile(filename, url, chat_id, ScriptLocationPath):
    try:
        f=open(ScriptLocationPath+"/"+str(chat_id)+"_telegram-shell-status.json", "r")  #Check if this chat has a previous location
        data = json.load(f)
        currentLocation = data['PATH']
        f.close()
    except:
        currentLocation = "/home"
    os.chdir(currentLocation)
    r= requests.get(url)
    open(filename, 'wb').write(r.content)
    resp="upload Completed \n\n" + Basicfunctions.ls_function(chat_id, ScriptLocationPath)
    return resp
