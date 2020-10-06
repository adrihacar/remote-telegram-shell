#!/usr/bin/env python3
import urllib.request
from time import sleep
import telegram
from telegram import ParseMode
import os
import json
import sys


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
    global chat_id

    try:
        data = json.load(f) #check the json is a valid one
        token = data['TOKEN']
        chat_id = data['CHAT_ID']
    except:
        print("Format of the configuration file is not correct", file=sys.stderr)
        sys.exit(1)
    
    
	
def get_ip():
 return urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')


def send_message(msg, chat_id):
    bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=ParseMode.HTML)
 

def check_telegram():
    while True:
        global update_id
        # Request updates after the last update_id
        for update in bot.get_updates(offset=update_id, timeout=10):
            update_id = update.update_id + 1
            if update.message:  # your bot can receive updates without messages
                msg=update.message.text
                print(msg) #The command is printed
                if(msg == "ip" or msg == "Ip"):
                    ip=get_ip()
                    send_message(ip,chat_id)
                else:
                    resp = os.popen(msg).read()
                    if(resp != ""):
                        send_message(resp,chat_id)

 
        sleep(4)
 
init()
check_telegram()
