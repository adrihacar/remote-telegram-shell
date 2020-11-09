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

def File(update, bot, type):
    aux=getattr(update.message, type)
    if (type=="document"):
        filename=aux.file_name
        url=telegram.Bot.get_file(bot,file_id=aux.file_id).file_path
        r= requests.get(url)
        return r, filename 
    else: #photos and videos don't have filename so it is generated from msgID
        msgID=update.message.message_id
        if (type=="video"):
            extension=aux.mime_type.split('/')[1]
            filename= str(msgID)+"."+extension   
            url=telegram.Bot.get_file(bot,file_id=aux.file_id).file_path        
        elif (type=="photo"):
            filename= str(msgID)+".jpg" #photo files don't come with extension so it will be always identified as jpg
            url=telegram.Bot.get_file(bot,file_id=aux[0].file_id).file_path #the json received from Telegram is diferent 
        
        r= requests.get(url)
        return r, filename

def downloadFile(update, chat_id, ScriptLocationPath, bot):
    try:
        f=open(ScriptLocationPath+"/"+str(chat_id)+"_telegram-shell-status.json", "r")  #Check if this chat has a previous location
        data = json.load(f)
        currentLocation = data['PATH']
        f.close()
    except:
        currentLocation = "/home"
    os.chdir(currentLocation)
    if(update.message.video != None):    #Checking kind of attachment
        name_content=File(update, bot, "video") #obtaining name and url
    elif(update.message.document != None):
        name_content=File(update, bot, "document")
    elif(update.message.photo != None):
        name_content=File(update, bot, "photo")
    open(name_content[1], 'wb').write(name_content[0].content) #Saving (be carefull it will not check it the file already exists)
    resp="upload Completed, saved with name "+name_content[1]+"\n\n" + Basicfunctions.ls_function(chat_id, ScriptLocationPath)
    return resp

