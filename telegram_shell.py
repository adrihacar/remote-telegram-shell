#!/usr/bin/env python3
import urllib.request
from time import sleep
import telegram
from telegram import ParseMode
import os
import json
import sys
import re


def init():
    read_conf_file()
    global bot
    global update_id
    bot=telegram.Bot(token)
    try:
       update_id = bot.get_updates()[0].update_id+1
    except IndexError:
        update_id = None

def read_conf_file():
    try:
    	#place route to configuration file here
        f = open(os.environ['HOME']+'/.config/telegram-shell/telegram-shell-conf.json') #
    except FileNotFoundError:
        print("Configuration file not found", file=sys.stderr)
        sys.exit(1)

    global token
    global chat_id_config

    try:
        data = json.load(f) #check the json is a valid one
        token = data['TOKEN']
        chat_id_config = data['CHAT_ID']
    except:
        print("Format of the configuration file is not correct", file=sys.stderr)
        sys.exit(1)
    
    
	
def get_ip():
 return urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')


def send_message(msg, chat_id):
    bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=ParseMode.HTML)
 
def answer_telegram (msg, chat_id):
    if(msg.lower() == "ip"):
                    ip=get_ip()
                    send_message(ip,chat_id)
                elif(re.match("cd .*", msg.lower())):  #cd command
                    folder = msg.lower().split("cd ")
                    os.chdir(folder[1])
                    resp = os.popen("ls").read()
                    send_message(resp,chat_id)      
                else:
                    print(msg)
                    resp = os.popen(msg).read()
                    if(resp != ""):
                        send_message(resp,chat_id)
                    else: ### In case the command should be lower letters
                        resp = os.popen(msg.lower()).read()
                        if(resp != ""):
                            send_message(resp,chat_id)
                        else:  ### In case the command isnt't available or not exists
                            resp = "Command not available"
                            send_message(resp,chat_id)
    
def check_telegram_dinamic_ChatID():
    while True:
        global update_id
        global chat_id
        # Request updates after the last update_id
        for update in bot.get_updates(offset=update_id, timeout=10):
            update_id = update.update_id + 1
            if update.message:  # your bot can receive updates without messages
                msg=update.message.text
                chat_id=update.message.chat.id
                """"""""
                print(update) #!! USELESS, JUST FOR DEVELOPMENT REASONS
                
                """"""""
                print(msg) #The command is printed
                answer_telegram (msg, chat_id)
                
        sleep(4)

def check_telegram():
    while True:
        global update_id
        # Request updates after the last update_id
        for update in bot.get_updates(offset=update_id, timeout=10):
            update_id = update.update_id + 1
            if (str(update.message.chat.id) == chat_id_config):   #Check if the chat ID is the one configured if not, ignore the message
                if update.message:  # your bot can receive updates without messages
                    msg=update.message.text
                    print(msg) #The command is printed
                    
                    answer_telegram (msg, chat_id_config)
        sleep(4)

init()
print(len(chat_id_config))
if(len(chat_id_config) < 1):
    check_telegram_dinamic_ChatID()
else:
    check_telegram()