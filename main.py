import telegram.ext
from dotenv import load_dotenv
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pdfkit
import logging
from telegram import Update
from jinja2 import Template
from pdfkit import from_string
import random
import requests
import fcntl
from bs4 import BeautifulSoup
import sys
from time import sleep
from flask import Flask, request



load_dotenv()
TOKEN = os.getenv("TOKEN")
OWNER_ID = '1608306485'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
# Dictionary to store user-password associations (using in-memory storage for simplicity)
user_auth_status = {}  # Track whether a user is authenticated
used_passwords = set()  # Track used passwords
valid_passwords = {}
Report_bug = {}
Suggestion = {}
Suggestion_reply = {}
proxy_url = 'http://vmzyukac:hxdsqnwzmv2w@45.94.47.66:8110'
app = Flask(__name__)
lock_file_path = '/user_input/lock_file.txt'
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
def acquire_lock():
    try:
        # Create the lock file
        with open(lock_file_path, 'w') as lock_file:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            print("Lock acquired.")
            return lock_file
    except (OSError, IOError):
        print("Lock acquisition failed. Another process may hold the lock.")
        return None

def release_lock(lock_file):
    try:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()
        print("Lock released.")
    except Exception as e:
        print(f"Error releasing lock: {e}")

# Example usage
lock_file = acquire_lock()

if lock_file:
    # Perform your operations here
    print("Performing operations while holding the lock.")

    # Release the lock when done
    release_lock(lock_file)

# Define a function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("You are already authenticated.")
    else:
        update.message.reply_text("Please enter the password to authenticate.")

def password_input(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in user_auth_status and user_id in valid_passwords:  # If the user is already authenticated
        update.message.reply_text("You are already authenticated.")
    else:
        password = update.message.text
        if password in valid_passwords and password not in used_passwords:
            # Mark the password as used
            used_passwords.add(password)
            # Mark the user as authenticated
            user_auth_status[user_id] = str(password)
            update.message.reply_text("You have been successfully authenticated.")
        else:
            update.message.reply_text("Incorrect password. Please try again.")

def add_password(update:Updater, context: CallbackContext ):
   if str(update.effective_user.id) == OWNER_ID: 
      if update.message.text == '/add_password':
        update.message.reply_text("Follow a valid Syntax: /add_password NewPassword")  
      else:
        input_text = update.message.text.split(' ')
        password = input_text[1]
        if password in valid_passwords:
           update.message.reply_text("Password is Already Existed")
        else:
           valid_passwords[password] = True
           update.message.reply_text(f"Password [{password}] Added successfully")
   else:
        update.message.reply_text("Sorry, you are not authorized to perform this action.")

def delete_password(update:Updater, context: CallbackContext ):
    if str(update.effective_user.id) == OWNER_ID:
      if update.message.text == '/delete_password':
        update.message.reply_text("Follow a valid Syntax: /delete_password ExistingPassword")  
      else:
        input_text = update.message.text.split(' ')
        index = input_text[1]
        if index in valid_passwords:
            del valid_passwords[index]
            update.message.reply_text(f"Password [{index}]deleted successfully!")
        else:
            update.message.reply_text("No password found for this chat.")
    else:
        update.message.reply_text("Sorry, you are not authorized to perform this action.")

def user_auth_status_command(update:Updater, context: CallbackContext ):
    if str(update.effective_user.id) == OWNER_ID:
        update.message.reply_text(user_auth_status)
    else:
       update.message.reply_text("You can not perform these operation")

def valid_passwords_command(update:Updater, context: CallbackContext ):
    if str(update.effective_user.id) == OWNER_ID:
        update.message.reply_text(valid_passwords)
    else:
       update.message.reply_text("You can not perform these operation")

def user_auth_status_delete_command(update:Updater, context: CallbackContext) -> None:
    if str(update.effective_user.id) == OWNER_ID:
      if update.message.text == '/user_auth_status_delete':
        update.message.reply_text("Follow a valid Syntax: /user_auth_status user_id")  
      else:
        input_text = update.message.text.split(' ')
        index = input_text[1]
        if int(index) in user_auth_status:
            del user_auth_status[int(index)]
            update.message.reply_text(user_auth_status)
            update.message.reply_text("User id Successfully moved Authentication to UnAuthentication!")
        else:
           update.message.reply_text("User ID not exist in Authentication")    
    else:
       update.message.reply_text("You can not perform these operation")

def Report_bug_command(update:Updater, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status: # If the user is not authenticated
           update.message.reply_text("Please authenticate first by entering the password.")
    else:    
        if update.message.text == '/Report_bug':
           update.message.reply_text("Report a bug to the owner and get one Month Free. Syntax: /Report_bug|Describe your bug")
        else:
           input = update.message.text.split('|')
           Key = input[1]
           Report_bug[user_id] = str(Key)
           update.message.reply_text("Bug Reported Successfully✅")

def Report_bug_check_command(update:Updater, context: CallbackContext) -> None:
        if str(update.effective_user.id) == OWNER_ID:
          update.message.reply_text(Report_bug)
        else:
          update.message.reply_text("You can not perform these operation")

def Report_bug_delete_command(update:Updater, context: CallbackContext) -> None:
    if str(update.effective_user.id) == OWNER_ID:
       if update.message.text == '/Report_bug_delete':
           update.message.reply_text("Report a bug to the owner and get one Month Free. Syntax: /Report_bug_delete user_id")
       else:
        input_text = update.message.text.split(' ')
        index = input_text[1]
        if int(index) in Report_bug:
            del Report_bug[int(index)]
            update.message.reply_text(Report_bug)
            update.message.reply_text("Bug Report Successfully Fixed")
        else:
           update.message.reply_text("User ID not exist in Bug Reports!")    
    else:
       update.message.reply_text("You can not perform these operation")

def Suggestion_command(update:Updater, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status: # If the user is not authenticated
           update.message.reply_text("Please authenticate first by entering the password.")
    else:    
        if update.message.text == '/Suggestion':
           update.message.reply_text("Suggest one or more features. You can see that feature in Future .If it approved get one Month Free!. Syntax: /Suggestion|Describe your bug")
        else:
           input = update.message.text.split('|')
           Key = input[1]
           if len('|') == 1:
              Suggestion[user_id] = str(Key)
              update.message.reply_text("Suggestion Added Successfully✅")
           else:
              update.message.reply_text("Invalid Format Please give your Suggestion in valid Format!")
def Suggestion_check_command(update:Updater, context: CallbackContext) -> None:
        if str(update.effective_user.id) == OWNER_ID:
          update.message.reply_text(Suggestion)
        else:
          update.message.reply_text("You can not perform these operation")

def Suggestion_reply_command(update:Updater, context:CallbackContext) -> None:
    if str(update.effective_user.id) == OWNER_ID:
      if update.message.text == '/Suggestion_reply':
        update.message.reply_text("Follow a valid Syntax: /Suggestion_reply|user_id|Description")  
      else:
        input_text = update.message.text.split('|')
        index = input_text[1]
        Reply = input_text[2]
        if int(index) in Suggestion:
            Suggestion_reply[int(index)] = str(Reply)
            update.message.reply_text(Suggestion_reply[int(index)])
            update.message.reply_text("Suggestion Conservation is Started")
        else:
           update.message.reply_text("User ID not exist in Suggestion!")    
    else:
       update.message.reply_text("You can not perform these operation")

def Suggestion_check_reply_command(update:Updater, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:
           update.message.reply_text("Please authenticate first by entering the password.")
    else:   
         if int(user_id) in Suggestion_reply:
            update.message.reply_text(Suggestion_reply[int(user_id)])
         elif int(user_id) not in Suggestion and int(user_id) not in Suggestion_reply:
            update.message.reply_text("You are not suggest any Featuure!")
         else:
            update.message.reply_text("No Reply on Your Suggestion!")

def send_update(update: Update, context: CallbackContext):
      # Get the message to send from the command
    if str(update.effective_user.id) == OWNER_ID:
      if update.message.text == '/send_update':
        update.message.reply_text("Follow a valid Syntax: /send_update|Description")  
      else:
        input_text = update.message.text.split('|')
        message_to_send = input_text[1]
      for user_id in user_auth_status: 
          context.bot.send_message(chat_id=user_id, text=message_to_send)
    else:
       update.message.reply_text("You can not perform these operation")

def help_command(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status: # If the user is not authenticated
           update.message.reply_text("Please authenticate first by entering the password.")
    else:    
        update.message.reply_text("""✨🌟💫            ✨🌟💫                   ✨🌟💫
🆕 /Guide - Provide a Guide\n#️⃣ /tag - Provide Player info\n🧾 /receipt - Provide any Receipts\n📱 /device - Provide Account Devices\n📝 /Report_bug - Report a Bug\n🗯 /Suggestion - Give any Suggestion\n ↪️ /Suggestion_check_reply - Check your Suggestion Reply\n♕ /help_owner - Owners Help Portal
✨🌟💫            ✨🌟💫                   ✨🌟💫""")
  
def help_owner_command(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) == OWNER_ID:
        update.message.reply_text("""✨🌟💫            ✨🌟💫                   ✨🌟💫
🆕 /Guide - Provide a Guide\n#️⃣ /tag - Provide Player info\n🧾 /receipt - Provide any Receipts\n📱 /device - Provide Account Devices\n🆕 /add_password - Add a new Password\n🗑️ /delete_password - Delete a Password\n👥 /user_auth_status - Check Authenticated Users\n🗑️ /user_auth_status_delete - Delete a Authenticated User\n🔐 /valid_passwords - Check all valid Passwords\n📝 /Report_bug - Report a Bug\n🎯 /Report_bug_check - Check Reported Bugs\n🗑️ /Report_bug_delete - Delete a Report of Bug\n🗯 /Suggestion - Give any Suggestion\n↪️ /Suggestion_check_reply - Check your Suggestion Reply\n↪️ /Suggestion_reply - Reply the Suggestions\n👥 /Suggestion_check - Check all the Suggestions\n /send_update - To update the Common  Message✨🌟💫            ✨🌟💫                   ✨🌟💫""")
    else:
       update.message.reply_text("You can not perform these operation")
def receipt(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is not authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else: 
        update.message.reply_text("""✨🌟💫            ✨🌟💫                   ✨🌟💫
🧾You want to generate receipt or bypass the receipt🎣\n🧬For Generate receipt /generate_receipt 
\n🎣For Bypass the receipt /Bypass_receipt\n✨🌟💫            ✨🌟💫                   ✨🌟💫""")
 
def Bypass_receipt(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is not authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:
        update.message.reply_text("Bypasses Getting Ready...")
        context.bot.send_document(chat_id=update.effective_chat.id, document=open('Bypass.doc', 'rb'))
        print("PDF SENDED!")
     
     
def generate_receipt(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:    
        update.message.reply_text("✨🌟💫            ✨🌟💫                   ✨🌟💫\nWhich receipt you want\n🧾For Google Receipt /Google_receipt\n🧾For Apple Receipt /Apple_receipt\n✨🌟💫            ✨🌟💫                   ✨🌟💫")

def Google_receipt(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else: 
        update.message.reply_text("""✨🌟💫            ✨🌟💫                   ✨🌟💫
🤖 Hey! I am here to generate Google receipt for you,🧾
👉 Now, I need some specific data what you want in Google receipt.📱
🌟 Please Enter your data with Sequence Syntax like :- /data_google|Order ID|date or month (If you want to add time you can add also)|Item name|Item price (Enter Item Price according to your curruncy or country and add also currency Symbol)🧾
💫 (Example:- /data_google|7393-8393-8499-83938|September 2022|Gold Pass|$4.99)🧾
💫 (Example:- /data_google|8393-8393-8389-10138|01 January 2022|Gold Pass|₹449.00)🧾
✨🌟💫            ✨🌟💫                   ✨🌟💫""")

def data_google(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:    
        if update.message.text == '/data_google':
           update.message.reply_text("Please Enter the information according to Syntax.\n(Syntax:- /data_google|Order-number|Month or date(if You want time then add time also)|Item-name|Item-price with thier currency symbol!)\n(Example: /data_google|3738-3638-3738-37388|Feb 24, 2023 1:24:40 PM|Royal Pass|$499.00)")
        else:   
            input_text = update.message.text.split("|")
            if len(input_text) == 5:
                order_number = input_text[1]
                month = input_text[2]
                Item_name = input_text[3]
                Item_price = input_text[4]  
                Item = Item_price[0]
                update.message.reply_text('Data Confirm reciept is genrating...✅')
                update.message.reply_text("preparing file...🧬")
                if Item == '₹':
                    Item_price1 = Item_price.replace('₹', '')
                    with open('Receipts/google_receipt.html', 'r') as file:
                     html_content=file.read()
                    modified_html = html_content.replace('{{order_number}}', order_number)
                    with open('user_input/user_inputs.html', 'w') as file:
                        file.write(modified_html)
                    with open('user_input/user_inputs.html', 'r') as file:
                      html_content = file.read()
                      modified_html = html_content.replace('{{month}}', month)
                    with open('user_input/user_inputs1.html', 'w') as file:
                        file.write(modified_html)
                    with open('user_input/user_inputs1.html', 'r') as file:
                      html_content = file.read()
                      modified_html = html_content.replace('{{Item_name}}', Item_name)
                    with open('user_input/user_inputs2.html', 'w') as file:
                        file.write(modified_html)
                    with open('user_input/user_inputs2.html', 'r') as file:
                      html_content = file.read()
                      modified_html = html_content.replace('{{Item_price}}', Item_price1)
                    with open('user_input/user_inputs3.html', 'w') as file:
                        file.write(modified_html)
                    pdfkit.from_file('user_input/user_inputs3.html', 'user_input/output.pdf', configuration=config)
                    context.bot.send_document(chat_id=update.effective_chat.id, document=open('user_input/output.pdf', 'rb'))
                    print("pdf sended!")
                    update.message.reply_text('❎If File is still not download then tap to /download ❎')   
                else:
                    with open('Receipts/google1.1_receipt.html', 'r') as file:
                     html_content=file.read()
                    modified_html = html_content.replace('{{order_number}}', order_number)
                    with open('user_input/user_inputs.html', 'w') as file:
                        file.write(modified_html)
                    with open('user_input/user_inputs.html', 'r') as file:
                      html_content = file.read()
                      modified_html = html_content.replace('{{month}}', month)
                    with open('user_input/user_inputs1.html', 'w') as file:
                        file.write(modified_html)
                    with open('user_input/user_inputs1.html', 'r') as file:
                      html_content = file.read()
                      modified_html = html_content.replace('{{Item_name}}', Item_name)
                    with open('user_input/user_inputs2.html', 'w') as file:
                        file.write(modified_html)
                    with open('user_input/user_inputs2.html', 'r') as file:
                      html_content = file.read()
                      modified_html = html_content.replace('{{Item_price}}', Item_price)
                    with open('user_input/user_inputs3.html', 'w') as file:
                        file.write(modified_html)
                    pdfkit.from_file('user_input/user_inputs3.html', 'user_input/output.pdf', configuration=config)
                    context.bot.send_document(chat_id=update.effective_chat.id, document=open('user_input/output.pdf', 'rb'))
                    print("pdf sended!")
                    update.message.reply_text('❎If File is still not download then tap to /download ❎')
            else:
               update.message.reply_text("I Think you forgot the Pipe ('|') .Please Give data in Valid Format")

def Apple_receipt(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:    
        update.message.reply_text('''✨🌟💫            ✨🌟💫                   ✨🌟💫
Choose One of it\n🧾For New Apple Receipts:\n/Apple_receipt_1\n🧾For old Apple Receipt:\n/Apple_receipt_2
✨🌟💫            ✨🌟💫                   ✨🌟💫''')

def Apple_receipt_1(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:    
        update.message.reply_text("""✨🌟💫            ✨🌟💫                   ✨🌟💫
🤖 Hey! I am here to generate Apple receipt for you,🧾
👉 Now, I need some specific data what you want in Apple receipt.📱
🌟 Please Enter your data with Sequence Syntax like :- /data_apple1|Order ID|date or month (If you want to add time you can add also)|Item name|Item price (Enter Item Price according to your curruncy or country and add also currency Symbol)🧾
💫 (Example:- /data_apple1|HKNH93BDK9D|September 2022|Gold Pass|$4.99)🧾
💫 (Example:- /data_apple1|NDKF93BDN3J|01 January 2022|Gold Pass|₹449.00)🧾
✨🌟💫            ✨🌟💫                   ✨🌟💫""")

def data_apple1(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:
        if update.message.text == '/data_apple1':
           update.message.reply_text("Please Enter the information according to Syntax.\n(Syntax:- /data_apple1|Order-number|Month or date(if You want time then add time also)|Item-name|Item-price with thier currency symbol!)")
        else:    
            input_text = update.message.text.split("|")
            if len(input_text) == 5:
                    order_number = input_text[1]
                    month = input_text[2]
                    Item_name = input_text[3]
                    Item_price = input_text[4]  
                    Item = Item_price[0]
                    update.message.reply_text('Data Confirm reciept is genrating...✅')
                    update.message.reply_text("preparing file...🧬")
                    if Item == '₹':
                        Item_price1 = Item_price.replace('₹', '')
                        with open('Receipts/apple1_receipt.html', 'r') as file:
                         html_content=file.read()
                        modified_html = html_content.replace('{{order_number}}', order_number)
                        with open('user_input/user_inputs.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{month}}', month)
                        with open('user_input/user_inputs1.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs1.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{Item_name}}', Item_name)
                        with open('user_input/user_inputs2.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs2.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{Item_price}}', Item_price1)
                        with open('user_input/user_inputs3.html', 'w') as file:
                            file.write(modified_html)
                        pdfkit.from_file('user_input/user_inputs3.html', 'user_input/output.pdf', configuration=config)
                        context.bot.send_document(chat_id=update.effective_chat.id, document=open('user_input/output.pdf', 'rb'))
                        print("pdf sended!")
                        update.message.reply_text('❎If File is still not download then tap to /download ❎')   
                    else:
                        with open('Receipts/apple1.1_receipt.html', 'r') as file:
                         html_content=file.read()
                        modified_html = html_content.replace('{{order_number}}', order_number)
                        with open('user_input/user_inputs.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{month}}', month)
                        with open('user_input/user_inputs1.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs1.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{Item_name}}', Item_name)
                        with open('user_input/user_inputs2.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs2.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{Item_price}}', Item_price)
                        with open('user_input/user_inputs3.html', 'w') as file:
                            file.write(modified_html)
                        pdfkit.from_file('user_input/user_inputs3.html', 'user_input/output.pdf', configuration=config)
                        context.bot.send_document(chat_id=update.effective_chat.id, document=open('user_input/output.pdf', 'rb'))
                        print("pdf sended!")
                        update.message.reply_text('❎If File is still not download then tap to /download ❎')
            else:
                   update.message.reply_text("I Think you forgot the Pipe ('|') .Please Give data in Valid Format")

def Apple_receipt_2(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:
        update.message.reply_text("""✨🌟💫            ✨🌟💫                   ✨🌟💫
🤖 Hey! I am here to generate Apple receipt for you,🧾
👉 Now, I need some specific data what you want in Apple receipt.📱
🌟 Please Enter your data with Sequence Syntax like :- /data_apple2|Order ID|date or month (If you want to add time you can add also)|Item name|Item price (Enter Item Price according to your curruncy or country and add also currency Symbol)🧾
💫 (Example:- /data_apple2|HKNH93BDK9D|September 2022|Gold Pass|$4.99)🧾
💫 (Example:- /data_apple2|NDKF93BDN3J|01 January 2022|Gold Pass|₹449.00)🧾
✨🌟💫            ✨🌟💫                   ✨🌟💫""")
def data_apple2(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:
        if update.message.text == '/data_apple2':
           update.message.reply_text("Please Enter the information according to Syntax.\n(Syntax:- /data_apple2|Order-number|Month or date(if You want time then add time also)|Item-name|Item-price with thier currency symbol!)")
        else:
            input_text = update.message.text.split("|")
            if len(input_text) == 5:
                    order_number = input_text[1]
                    month = input_text[2]
                    Item_name = input_text[3]
                    Item_price = input_text[4]  
                    Item = Item_price[0]
                    update.message.reply_text('Data Confirm reciept is genrating...✅')
                    update.message.reply_text("preparing file...🧬")
                    if Item == '₹':
                        Item_price1 = Item_price.replace('₹', '')
                        with open('Receipts/apple2_receipt.html', 'r') as file:
                         html_content=file.read()
                        modified_html = html_content.replace('{{order_number}}', order_number)
                        with open('user_input/user_inputs.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{month}}', month)
                        with open('user_input/user_inputs1.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs1.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{Item_name}}', Item_name)
                        with open('user_input/user_inputs2.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs2.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{Item_price}}', Item_price1)
                        with open('user_input/user_inputs3.html', 'w') as file:
                            file.write(modified_html)
                        pdfkit.from_file('user_input/user_inputs3.html', 'user_input/output.pdf', configuration=config)
                        context.bot.send_document(chat_id=update.effective_chat.id, document=open('user_input/output.pdf', 'rb'))
                        print("pdf sended!")
                        update.message.reply_text('❎If File is still not download then tap to /download ❎')   
                    else:
                        with open('Receipts/apple2.1_receipt.html', 'r') as file:
                         html_content=file.read()
                        modified_html = html_content.replace('{{order_number}}', order_number)
                        with open('user_input/user_inputs.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{month}}', month)
                        with open('user_input/user_inputs1.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs1.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{Item_name}}', Item_name)
                        with open('user_input/user_inputs2.html', 'w') as file:
                            file.write(modified_html)
                        with open('user_input/user_inputs2.html', 'r') as file:
                          html_content = file.read()
                          modified_html = html_content.replace('{{Item_price}}', Item_price)
                        with open('user_input/user_inputs3.html', 'w') as file:
                            file.write(modified_html)
                        pdfkit.from_file('user_input/user_inputs3.html', 'user_input/output.pdf', configuration=config)
                        context.bot.send_document(chat_id=update.effective_chat.id, document=open('user_input/output.pdf', 'rb'))
                        print("pdf sended!")
                        update.message.reply_text('❎If File is still not download then tap to /download ❎')
            else:
                   update.message.reply_text("I Think you forgot the Pipe ('|') .Please Give data in Valid Format")
def device(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:
        update.message.reply_text("""✨🌟💫            ✨🌟💫                   ✨🌟💫
🎣Enter the tag:📱
/generate_devices yourtag
Example:- /generate_devices 2pp
✨🌟💫            ✨🌟💫                   ✨🌟💫""")
   

def generate_devices(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:
        # Get user input for the key or slicing number
        if update.message.text == '/generate_devices':
            update.message.reply_text("Follow a valid Syntax: /generate_devices yourtag")
        else:
            input = update.message.text.split(' ')
            tag = input[1]
            tag_without_hash = tag.replace('#', '')
            cos1_url_name = f"https://www.clashofstats.com/players/{tag_without_hash}/summary"
            response = requests.get(cos1_url_name, proxies={'http': proxy_url, 'https': proxy_url})
            if response.status_code == 200:
                update.message.reply_text(f"Tag [{tag}] is Collected✅")
                if len(tag_without_hash) == 9:
                  first_letter = tag_without_hash[0]
                  if first_letter == '2':
                      Creation_date = "2014"
                  elif first_letter == '8':
                      Creation_date = "2014"
                  elif first_letter == '9':
                      Creation_date = "2015"
                  elif first_letter == 'P':
                      Creation_date = "2016"
                  elif first_letter == 'Y':
                      Creation_date = "2017"
                  elif first_letter == 'L':
                      Creation_date = "2018"
                  elif first_letter == 'Q':
                      Creation_date = "2019"
                  else:
                      Creation_date = "2014"
                elif len(tag_without_hash) == 8:
                    first_letter = tag_without_hash[0]
                    if first_letter == 'Q':
                        Creation_date = "2012"
                    elif first_letter == 'G':
                        Creation_date = "2012"
                    elif first_letter == 'R':
                        Creation_date = "2012"
                    elif first_letter == 'v':
                        Creation_date = "2013"
                    elif first_letter == 'P':
                        Creation_date = "2013"
                    elif first_letter == '9':
                        Creation_date = "2013"
                    elif first_letter == '8':
                        Creation_date = "2013"
                    elif first_letter == 'J':
                        Creation_date = "2013"
                    else:
                        Creation_date = "2013"
                elif len(tag_without_hash) == 7:
                    first_letter = tag_without_hash[0]
                    if first_letter == 'U':
                        Creation_date = "2011"
                    elif first_letter == '2':
                        Creation_date = "2011"
                    elif first_letter == 'L':
                        Creation_date = "2011"
                    else:
                        Creation_date = "2012"
                elif len(tag_without_hash) == 6:
                    first_letter = tag_without_hash[0]
                    if first_letter == 'U':
                        Creation_date = "2011"
                    elif first_letter:
                        Creation_date = "2011"
                    else:
                        Creation_date = "2011"
                else:
                   Creation_date = "2010"
                user_input = Creation_date

                #Location
                coc_url_location = f"https://www.clashofstats.com/players/{tag_without_hash}/history/"
                response = requests.get(coc_url_location, proxies={'http': proxy_url, 'https': proxy_url})
                if response.status_code == 200:
                  soup = BeautifulSoup(response.text, 'html.parser')
                  span_element = soup.find('span', class_='text--secondary caption')
                  if span_element:
                    clan_tag = span_element.text.strip()
                    translation_table = str.maketrans("", "", "-# ")
                    clan_tag_ = clan_tag.translate(translation_table)
                  else:
                    clan_tag_ = "NA"
                else:
                   clan_tag_ = ("NA")
                cos_url_loaction1 = f"https://www.clashofstats.com/clans/{clan_tag_}/history/past-members?filter=%23{tag_without_hash}"
                if response.status_code == 200:
                    response = requests.get(cos_url_loaction1, proxies={'http': proxy_url, 'https': proxy_url})
                    soup = BeautifulSoup(response.text, 'html.parser')
                    span_elements = soup.find_all('span', class_='num-val')
                    if len(span_elements) >= 3:
                        country_clan = span_elements[2].text.strip()
                    else:
                     country_clan = ("International")
                else:
                   country_clan = ("International")
                United_State_of_America = {
                '2010':["iPad 1", "iPhone 4", "Samsung Galaxy S (GT-I9000)", "Samsung Galaxy Tab (GT-P1000)"],
                '2011':["iPad 2", "iPhone 4S", "Samsung Galaxy S II (GT-I9100)", "Samsung Galaxy Note (GT-N7000)"],
                '2012':["iPad 3", "iPad 4", "iPhone 5", "Samsung Galaxy S III (GT-I9300)", "Samsung Galaxy Note II (GT-N7100)", ],
                '2013':["iPad Air",  "iphone5S", "iphone5C", "Samsung Galaxy S4 (GT-I9500)", "Samsung Galaxy Note 3 (SM-N900)", "Samsung Galaxy J (GT-I9300I)", ],
                '2014':["iPad Air 2", "iphone 6 / 6 Plus", "Samsung Galaxy S5 (SM-G900F)", "Samsung Galaxy Note 4 (SM-N910)", "Samsung Galaxy A3 (SM-A300)", "Samsung Galaxy J1 (SM-J100)",  ],
                '2015':["iPad Pro (12.9-inch)", "iphone 6S / 6s Plus", "Samsung Galaxy Note 5 (SM-N920)", "Samsung Galaxy A5 (SM-A500)", "Samsung Galaxy J2 (SM-J200)",],
                '2016':["iPad Pro (9.7-inch)", "iphone SE (1st generation)", "iphone 7 / 7 Plus", "Samsung Galaxy Note 7 (discontinued)",  "Samsung Galaxy A7 (SM-A700)", "Samsung Galaxy J3 (SM-J320)", ],
                '2017':["iPad (5th generation)", "iPhone 8 / 8 Plus", "iPone X", "Samsung Galaxy S8 (SM-G950F)", "Samsung Galaxy Note 8 (SM-N950F)", "Samsung Galaxy A8 (SM-A800)", "Samsung Galaxy J5 (SM-J530)",],
                '2018':["iPad (6th generation)", "iPad Pro (3rd generation, 12.9-inch)", "iPad Pro (3rd generation, 11-inch)", "iPhone XS /XS MAX", "iPhone XR", "Samsung Galaxy S9 (SM-G960F)", "Samsung Galaxy Note 9 (SM-N960F)", "Samsung Galaxy A9 (SM-A900)", "Samsung Galaxy J6 (SM-J600)"],
                '2019':["iPad Air (3rd generation)", "iPad Mini (5th generation)", "iPad (7th generation)", "iPhone 11 / 11 Pro / 11 Pro MAX", "Samsung Galaxy S10 (SM-G973F)", "Samsung Galaxy Note 10 (SM-N970F)", "Samsung Galaxy A10 (SM-A105)", "Samsung Galaxy M10 (SM-M105)", "Samsung Galaxy J7 (SM-J730)", ],
                '2020':["iPad Pro (4th generation, 12.9-inch)", "iPad Pro (4th generation, 11-inch)", "iPad (8th generation)", "iPad Air (4th generation)", "iphone SE (2nd generation)", "iPhone 12 / 12 Mini", "iPhone 12 Pro / 12 Pro Max", "Samsung Galaxy S20 (SM-G980F)", "Samsung Galaxy Note 20 (SM-N980F)", "Samsung Galaxy A11 (SM-A115)", "Samsung Galaxy M11 (SM-M115)", "Samsung Galaxy J8 (SM-J810)",],
                '2021':["iPad Pro (5th generation, 12.9-inch)", "iPad Pro (5th generation, 11-inch)", "iPad Mini (6th generation)", "iPhone 13 / 13 Mini", "iPhone 13 Pro / 13 Pro Max", "Samsung Galaxy S21 (SM-G991B)", "Samsung Galaxy Note 21 (expected)", "Samsung Galaxy A12 (SM-A125)", "Samsung Galaxy M12 (SM-M125)"],
                '2022':["iPad Air: 5th generation", "iPad Pro 12.9-inch: 6th generation", "iPhone SE (3rd generation)", "iPhone 14 / 14 Mini", "iPhone 14 Pro / 14 Pro Max", "Samsung Galaxy S22", "Samsung Galaxy Note 22", "Samsung Galaxy A13", "Samsung Galaxy M13"],
                '2023':["iPad 10th generation", "iPhone 15 / 15 Mini", "iPhone 15 Pro / 15 Pro Max", "Samsung Galaxy S23", "Samsung Galaxy Note 23 Ultra", "Samsung Galaxy A14", "Samsung Galaxy M14"],
                }
                Canada = {
                '2010':["BlackBerry Torch 9800", "BlackBerry Bold 9700", "BlackBerry Curve 8530", "BlackBerry Pearl 9100", "iPhone 4", "Samsung Galaxy S (GT-I9000)", "Samsung Galaxy Tab (GT-P1000)"],
                '2011':["BlackBerry Torch 9810", "BlackBerry Bold 9780", "BlackBerry Curve 3G 9300", "BlackBerry Pearl 9105", "iPhone 4S", "Samsung Galaxy S II (GT-I9100)", "Samsung Galaxy Note (GT-N7000)"],
                '2012':["BlackBerry Bold 9900", "BlackBerry Curve 9360", "iPhone 5", "Samsung Galaxy S III (GT-I9300)", "Samsung Galaxy Note II (GT-N7100)"],
                '2013':["BlackBerry Z10", "BlackBerry Q10", "iPhone 5S", "iPhone 5C", "Samsung Galaxy S4 (GT-I9500)", "Samsung Galaxy Note 3 (SM-N900)", "Samsung Galaxy J (GT-I9300I)"],
                '2014':["BlackBerry Passport", "iPhone 6 / 6 Plus", "Samsung Galaxy S5 (SM-G900F)", "Samsung Galaxy Note 4 (SM-N910)", "Samsung Galaxy A3 (SM-A300)", "Samsung Galaxy J1 (SM-J100)"],
                '2015':["BlackBerry Classic", "iPhone 6S / 6s Plus", "Samsung Galaxy Note 5 (SM-N920)", "Samsung Galaxy A5 (SM-A500)", "Samsung Galaxy J2 (SM-J200)"],
                '2016':["BlackBerry Priv", "iphone SE (1st generation)", "iphone 7 / 7 Plus", "Samsung Galaxy Note 7 (discontinued)", "Samsung Galaxy A7 (SM-A700)", "Samsung Galaxy J3 (SM-J320)"],
                '2017':["BlackBerry KeyOne", "iPhone 8 / 8 Plus", "iPone X", "Samsung Galaxy S8 (SM-G950F)", "Samsung Galaxy Note 8 (SM-N950F)", "Samsung Galaxy A8 (SM-A800)", "Samsung Galaxy J5 (SM-J530)"],
                '2018':["BlackBerry Key2", "iPhone XS /XS MAX", "iPhone XR", "Samsung Galaxy S9 (SM-G960F)", "Samsung Galaxy Note 9 (SM-N960F)", "Samsung Galaxy A9 (SM-A900)", "Samsung Galaxy J6 (SM-J600)"],
                '2019':["BlackBerry Key2 LE", "iPhone 11 / 11 Pro / 11 Pro MAX", "Samsung Galaxy S10 (SM-G973F)", "Samsung Galaxy Note 10 (SM-N970F)", "Samsung Galaxy A10 (SM-A105)", "Samsung Galaxy M10 (SM-M105)", "Samsung Galaxy J7 (SM-J730)"],
                '2020':["iPhone SE (2nd generation)", "iPhone 12 / 12 Mini", "iPhone 12 Pro / 12 Pro Max", "Samsung Galaxy S20 (SM-G980F)", "Samsung Galaxy Note 20 (SM-N980F)", "Samsung Galaxy A11 (SM-A115)", "Samsung Galaxy M11 (SM-M115)", "Samsung Galaxy J8 (SM-J810)"],
                '2021':["iPhone 13 / 13 Mini", "iPhone 13 Pro / 13 Pro Max", "Samsung Galaxy S21 (SM-G991B)", "Samsung Galaxy Note 21 (expected)", "Samsung Galaxy A12 (SM-A125)", "Samsung Galaxy M12 (SM-M125)"],
                '2022':["iPhone SE (3rd generation)", "iPhone 14 / 14 Mini", "iPhone 14 Pro / 14 Pro Max", "Samsung Galaxy S22", "Samsung Galaxy Note 22", "Samsung Galaxy A13", "Samsung Galaxy M13"],
                '2023':["iPhone 15 / 15 Mini", "iPhone 15 Pro / 15 Pro Max", "Samsung Galaxy S23", "Samsung Galaxy Note 23 Ultra", "Samsung Galaxy A14", "Samsung Galaxy M14"],
                }
                india_devices = {
                '2010': ["Nokia X6", "Nokia N8", "Samsung Galaxy S (GT-I9000)", "Samsung Galaxy Tab (GT-P1000)", "iPhone 4", "Xiaomi Mi 1"],
                '2011': ["Nokia E6", "Nokia C7", "Samsung Galaxy S II (GT-I9100)", "Samsung Galaxy Note (GT-N7000)", "iPhone 4S", "Xiaomi Mi 1S"],
                '2012': ["Nokia Lumia 800", "Nokia 808 PureView", "Samsung Galaxy S III (GT-I9300)", "Samsung Galaxy Note II (GT-N7100)", "iPhone 5", "Xiaomi Mi 2"],
                '2013': ["Nokia Lumia 920", "Nokia Lumia 520", "Samsung Galaxy S4 (GT-I9500)", "Samsung Galaxy Note 3 (SM-N900)", "iPhone 5S", "Xiaomi Mi 3"],
                '2014': ["Nokia Lumia 1020", "Nokia Lumia 1520", "Samsung Galaxy S5 (SM-G900F)", "Samsung Galaxy Note 4 (SM-N910)", "iPhone 6 / 6 Plus", "Xiaomi Mi 4"],
                '2015': ["Nokia Lumia 730", "Nokia Lumia 830", "Samsung Galaxy Note 5 (SM-N920)", "Samsung Galaxy A5 (SM-A500)", "iPhone 6S / 6s Plus", "Xiaomi Mi 4i"],
                '2016': ["Nokia Lumia 950", "Nokia 6", "Samsung Galaxy Note 7 (discontinued)", "Samsung Galaxy A7 (SM-A700)", "iPhone SE (1st generation)", "Xiaomi Mi 5"],
                '2017': ["Nokia 8", "Nokia 5", "Samsung Galaxy S8 (SM-G950F)", "Samsung Galaxy Note 8 (SM-N950F)", "iPhone 8 / 8 Plus", "Xiaomi Mi 6"],
                '2018': ["Nokia 7 Plus", "Nokia 6.1 Plus", "Samsung Galaxy S9 (SM-G960F)", "Samsung Galaxy Note 9 (SM-N960F)", "iPhone XS /XS MAX", "Xiaomi Mi 8"],
                '2019': ["Nokia 9 PureView", "Nokia 4.2", "Samsung Galaxy S10 (SM-G973F)", "Samsung Galaxy Note 10 (SM-N970F)", "iPhone 11 / 11 Pro / 11 Pro MAX", "Xiaomi Mi 9"],
                '2020': ["Nokia 5.3", "Nokia C3", "Samsung Galaxy S20 (SM-G980F)", "Samsung Galaxy Note 20 (SM-N980F)", "iPhone SE (2nd generation)", "Vivo V19", "Oppo Reno 3 Pro", "Realme 6", "Sony Xperia 1 II (XQ-AT51)", "Xiaomi Mi 10", "OnePlus 8"],
                '2021': ["Nokia G20", "Nokia C20 Plus", "Samsung Galaxy S21 (SM-G991B)", "Samsung Galaxy Note 21 (expected)", "iPhone 13 / 13 Mini", "Vivo V21", "Oppo F19 Pro", "Realme 8", "Sony Xperia 5 III (XQ-BC72)", "Xiaomi Mi 11", "OnePlus 9"],
                '2022': ["Nokia G50", "Nokia T20 Tablet", "Samsung Galaxy S22", "Samsung Galaxy Note 22", "iPhone 14 / 14 Mini", "Vivo X60 Pro", "Oppo Find X4 Pro", "Realme GT 2 Pro", "Sony Xperia 1 III (XQ-BC62)", "Xiaomi Mi 11 Ultra", "OnePlus 10"],
                '2023': ["Nokia G70", "Nokia X20", "Samsung Galaxy S23", "Samsung Galaxy Note 23 Ultra", "iPhone 15 / 15 Mini", "Vivo X80 Pro", "Oppo Reno 7 Pro", "Realme 9 Pro", "Sony Xperia 10 IV (XQ-BC52)", "Xiaomi Mi 12", "OnePlus 11"],
                 }
                Japan= {
                '2010': ["Sony Xperia X10", "Sharp IS03", "Toshiba REGZA T-01C", "iPhone 4", "Samsung Galaxy S (SC-02B)"],
                '2011': ["Sony Xperia Arc", "Sharp Aquos Phone SH-12C", "Fujitsu ARROWS Z", "iPhone 4S", "Samsung Galaxy S II (SC-02C)"],
                '2012': ["Sony Xperia S", "Sharp Aquos Phone SH-06D", "Fujitsu ARROWS X", "iPhone 5", "Samsung Galaxy S III (SC-06D)"],
                '2013': ["Sony Xperia Z", "Sharp Aquos Phone Zeta SH-02E", "Fujitsu ARROWS NX", "iPhone 5S", "Samsung Galaxy S4 (SC-04E)"],
                '2014': ["Sony Xperia Z3", "Sharp Aquos Crystal", "Fujitsu ARROWS NX F-04G", "iPhone 6 / 6 Plus", "Samsung Galaxy S5 (SC-04F)"],
                '2015': ["Sony Xperia Z5", "Sharp Aquos Phone SH-04H", "Fujitsu ARROWS NX F-05F", "iPhone 6S / 6s Plus", "Samsung Galaxy S6 (SC-05G)"],
                '2016': ["Sony Xperia XZ", "Sharp Aquos R", "Fujitsu ARROWS NX F-01H", "iPhone SE (1st generation)", "Samsung Galaxy S7 (SC-02H)"],
                '2017': ["Sony Xperia XZ1", "Sharp Aquos S2", "Fujitsu ARROWS Be F-04K", "iPhone 8 / 8 Plus", "Samsung Galaxy S8 (SC-02J)"],
                '2018': ["Sony Xperia XZ2", "Sharp Aquos R2", "Fujitsu ARROWS NX F-01K", "iPhone XS / XS MAX", "Samsung Galaxy S9 (SC-02K)"],
                '2019': ["Sony Xperia 1", "Sharp Aquos R3", "Fujitsu ARROWS 5G", "iPhone 11 / 11 Pro / 11 Pro MAX", "Samsung Galaxy S10 (SC-03L)"],
                '2020': ["Sony Xperia 5 II", "Sharp Aquos R5G", "Fujitsu ARROWS 5G UW", "iPhone SE (2nd generation)", "Samsung Galaxy S20 (SC-51A)"],
                '2021': ["Sony Xperia 1 III", "Sharp Aquos R6", "Fujitsu ARROWS NX9 F-52A", "iPhone 13 / 13 Mini", "Samsung Galaxy S21 (SCG99J)"],
                '2022': ["Sony Xperia 5 III", "Sharp Aquos R7", "Fujitsu ARROWS Tab Q704/H", "iPhone 14 / 14 Mini", "Samsung Galaxy S22 (SCG99J)"],
                '2023': ["Sony Xperia 10 IV", "Sharp Aquos Sense5G", "Fujitsu ARROWS Tab Q508/S", "iPhone 15 / 15 Mini", "Samsung Galaxy S23 (SCG99J)"],
                 }
                Bangladesh = {
                '2010': ["iPhone 4", "Samsung Galaxy S (I9000)", "Nokia N8", "HTC Desire", "Sony Xperia X10", "BlackBerry Torch 9800"],
                '2011': ["iPhone 4S", "Samsung Galaxy S II (I9100)", "Nokia Lumia 800", "HTC Sensation", "Sony Xperia Arc", "BlackBerry Bold 9900"],
                '2012': ["iPhone 5", "Samsung Galaxy S III (I9300)", "Nokia Lumia 920", "HTC One X", "Sony Xperia S", "BlackBerry Z10"],
                '2013': ["iPhone 5S", "Samsung Galaxy S4 (I9500)", "Nokia Lumia 1020", "HTC One (M7)", "Sony Xperia Z", "BlackBerry Q10"],
                '2014': ["iPhone 6 / 6 Plus", "Samsung Galaxy S5 (SM-G900F)", "Nokia Lumia 1520", "HTC One M8", "Sony Xperia Z3", "BlackBerry Passport"],
                '2015': ["iPhone 6S / 6s Plus", "Samsung Galaxy S6 (SM-G920F)", "Nokia Lumia 930", "HTC One M9", "Sony Xperia Z5", "BlackBerry Priv"],
                '2016': ["iPhone SE (1st generation)", "Samsung Galaxy S7 (SM-G930F)", "Nokia 6", "HTC 10", "Sony Xperia XZ", "Google Pixel"],
                '2017': ["iPhone 8 / 8 Plus", "Samsung Galaxy S8 (SM-G950F)", "Nokia 8", "HTC U11", "Sony Xperia XZ1", "Google Pixel 2"],
                '2018': ["iPhone XS / XS Max", "Samsung Galaxy S9 (SM-G960F)", "Nokia 9 PureView", "HTC U12+", "Sony Xperia XZ2", "Google Pixel 3"],
                '2019': ["iPhone 11 / 11 Pro / 11 Pro Max", "Samsung Galaxy S10 (SM-G973F)", "Nokia 7.2", "HTC U12 Life", "Sony Xperia 1", "Google Pixel 4"],
                '2020': ["iPhone SE (2nd generation)", "Samsung Galaxy S20 (SM-G980F)", "Nokia 8.3", "OnePlus 8", "Sony Xperia 5 II", "Google Pixel 4a"],
                '2021': ["iPhone 13 / 13 Mini", "Samsung Galaxy S21 (SM-G991B)", "Nokia X20", "OnePlus 9", "Sony Xperia 1 III", "Google Pixel 5"],
                '2022': ["iPhone 14 / 14 Mini", "Samsung Galaxy S22", "Nokia G50", "OnePlus 10", "Sony Xperia 5 III", "Google Pixel 6"],
                '2023': ["iPhone 15 / 15 Mini", "Samsung Galaxy S23", "Nokia G70", "OnePlus 11", "Sony Xperia 10 IV", "Google Pixel 7"],
                 }        
                uk_devices = {
                '2010': ["iPhone 4", "Samsung Galaxy S (I9000)", "HTC Desire", "Nokia N8", "Sony Xperia X10", "BlackBerry Torch 9800"],
                '2011': ["iPhone 4S", "Samsung Galaxy S II (I9100)", "HTC Sensation", "Nokia Lumia 800", "Sony Xperia Arc", "BlackBerry Bold 9900"],
                '2012': ["iPhone 5", "Samsung Galaxy S III (I9300)", "HTC One X", "Nokia Lumia 920", "Sony Xperia S", "BlackBerry Z10"],
                '2013': ["iPhone 5S", "Samsung Galaxy S4 (I9500)", "HTC One (M7)", "Nokia Lumia 1020", "Sony Xperia Z", "BlackBerry Q10"],
                '2014': ["iPhone 6 / 6 Plus", "Samsung Galaxy S5 (SM-G900F)", "HTC One M8", "Nokia Lumia 1520", "Sony Xperia Z3", "BlackBerry Passport"],
                '2015': ["iPhone 6S / 6s Plus", "Samsung Galaxy S6 (SM-G920F)", "HTC One M9", "Nokia Lumia 930", "Sony Xperia Z5", "BlackBerry Priv"],
                '2016': ["iPhone SE (1st generation)", "Samsung Galaxy S7 (SM-G930F)", "HTC 10", "Nokia 6", "Sony Xperia XZ", "Google Pixel"],
                '2017': ["iPhone 8 / 8 Plus", "Samsung Galaxy S8 (SM-G950F)", "HTC U11", "Nokia 8", "Sony Xperia XZ1", "Google Pixel 2"],
                '2018': ["iPhone XS / XS Max", "Samsung Galaxy S9 (SM-G960F)", "HTC U12+", "Nokia 9 PureView", "Sony Xperia XZ2", "Google Pixel 3"],
                '2019': ["iPhone 11 / 11 Pro / 11 Pro Max", "Samsung Galaxy S10 (SM-G973F)", "HTC U12 Life", "Nokia 7.2", "Sony Xperia 1", "Google Pixel 4"],
                '2020': ["iPhone SE (2nd generation)", "Samsung Galaxy S20 (SM-G980F)", "Nokia 8.3", "OnePlus 8", "Sony Xperia 5 II", "Google Pixel 4a"],
                '2021': ["iPhone 13 / 13 Mini", "Samsung Galaxy S21 (SM-G991B)", "Nokia X20", "OnePlus 9", "Sony Xperia 1 III", "Google Pixel 5"],
                '2022': ["iPhone 14 / 14 Mini", "Samsung Galaxy S22", "Nokia G50", "OnePlus 10", "Sony Xperia 5 III", "Google Pixel 6"],
                '2023': ["iPhone 15 / 15 Mini", "Samsung Galaxy S23", "Nokia G70", "OnePlus 11", "Sony Xperia 10 IV", "Google Pixel 7"],
                 }
                International= {
                '2010': ["iPhone 4", "Samsung Galaxy S (I9000)", "HTC Desire", "Nokia N8", "Sony Xperia X10", "BlackBerry Torch 9800"],
                '2011': ["iPhone 4S", "Samsung Galaxy S II (I9100)", "HTC Sensation", "Nokia Lumia 800", "Sony Xperia Arc", "BlackBerry Bold 9900"],
                '2012': ["iPhone 5", "Samsung Galaxy S III (I9300)", "HTC One X", "Nokia Lumia 920", "Sony Xperia S", "BlackBerry Z10"],
                '2013': ["iPhone 5S", "Samsung Galaxy S4 (I9500)", "HTC One (M7)", "Nokia Lumia 1020", "Sony Xperia Z", "BlackBerry Q10"],
                '2014': ["iPhone 6 / 6 Plus", "Samsung Galaxy S5 (SM-G900F)", "HTC One M8", "Nokia Lumia 1520", "Sony Xperia Z3", "BlackBerry Passport"],
                '2015': ["iPhone 6S / 6s Plus", "Samsung Galaxy S6 (SM-G920F)", "HTC One M9", "Nokia Lumia 930", "Sony Xperia Z5", "BlackBerry Priv"],
                '2016': ["iPhone SE (1st generation)", "Samsung Galaxy S7 (SM-G930F)", "HTC 10", "Nokia 6", "Sony Xperia XZ", "Google Pixel"],
                '2017': ["iPhone 8 / 8 Plus", "Samsung Galaxy S8 (SM-G950F)", "HTC U11", "Nokia 8", "Sony Xperia XZ1", "Google Pixel 2"],
                '2018': ["iPhone XS / XS Max", "Samsung Galaxy S9 (SM-G960F)", "HTC U12+", "Nokia 9 PureView", "Sony Xperia XZ2", "Google Pixel 3"],
                '2019': ["iPhone 11 / 11 Pro / 11 Pro Max", "Samsung Galaxy S10 (SM-G973F)", "HTC U12 Life", "Nokia 7.2", "Sony Xperia 1", "Google Pixel 4"],
                '2020': ["iPhone SE (2nd generation)", "Samsung Galaxy S20 (SM-G980F)", "OnePlus 8", "Nokia 8.3", "Sony Xperia 5 II", "Google Pixel 4a"],
                '2021': ["iPhone 13 / 13 Mini", "Samsung Galaxy S21 (SM-G991B)", "OnePlus 9", "Nokia X20", "Sony Xperia 1 III", "Google Pixel 5"],
                '2022': ["iPhone 14 / 14 Mini", "Samsung Galaxy S22", "OnePlus 10", "Nokia G50", "Sony Xperia 5 III", "Google Pixel 6"],
                '2023': ["iPhone 15 / 15 Mini", "Samsung Galaxy S23", "OnePlus 11", "Nokia G70", "Sony Xperia 10 IV", "Google Pixel 7"],
                }
                france_devices = {
                '2010': ["iPhone 4", "Samsung Galaxy S", "iPad"],
                '2011': ["iPhone 4S", "Samsung Galaxy S II", "iPad 2"],
                '2012': ["iPhone 5", "Samsung Galaxy S III", "iPad 3", "Google Nexus 7"],
                '2013': ["iPhone 5S", "Samsung Galaxy S4", "iPad Air", "Sony Xperia Z"],
                '2014': ["iPhone 6 / 6 Plus", "Samsung Galaxy S5", "iPad Air 2", "LG G3"],
                '2015': ["iPhone 6S / 6S Plus", "Samsung Galaxy S6", "iPad Pro", "Huawei P8"],
                '2016': ["iPhone SE", "Samsung Galaxy S7", "iPad Pro (9.7-inch)", "Google Pixel"],
                '2017': ["iPhone 7 / 7 Plus", "Samsung Galaxy S8", "iPad (5th generation)", "OnePlus 5"],
                '2018': ["iPhone 8 / 8 Plus", "Samsung Galaxy S9", "iPad Pro (3rd generation)", "Huawei P20"],
                '2019': ["iPhone 11", "Samsung Galaxy S10", "iPad Air (3rd generation)", "Google Pixel 4"],
                '2020': ["iPhone SE (2nd generation)", "Samsung Galaxy S20", "iPad Pro (4th generation)", "OnePlus 8"],
                '2021': ["iPhone 12", "Samsung Galaxy S21", "iPad Pro (5th generation)", "Google Pixel 5"],
                '2022': ["iPhone 13", "Samsung Galaxy S22", "iPad Air (5th generation)", "Huawei P40"],
                '2023': ["iPhone 14", "Samsung Galaxy S23", "iPad (10th generation)", "OnePlus 10"]
                }
                finland_devices = {
                '2010': ["Nokia N8", "iPhone 4", "Samsung Galaxy S", "iPad"],
                '2011': ["Nokia Lumia 800", "iPhone 4S", "Samsung Galaxy S II", "iPad 2"],
                '2012': ["Nokia Lumia 920", "iPhone 5", "Samsung Galaxy S III", "iPad 3", "Google Nexus 7"],
                '2013': ["Nokia Lumia 1020", "iPhone 5S", "Samsung Galaxy S4", "iPad Air", "Sony Xperia Z"],
                '2014': ["Nokia Lumia 1520", "iPhone 6 / 6 Plus", "Samsung Galaxy S5", "iPad Air 2", "LG G3"],
                '2015': ["Nokia Lumia 930", "iPhone 6S / 6S Plus", "Samsung Galaxy S6", "iPad Pro", "Huawei P8"],
                '2016': ["Nokia 6", "iPhone SE", "Samsung Galaxy S7", "iPad Pro (9.7-inch)", "Google Pixel"],
                '2017': ["Nokia 8", "iPhone 7 / 7 Plus", "Samsung Galaxy S8", "iPad (5th generation)", "OnePlus 5"],
                '2018': ["Nokia 7 Plus", "iPhone 8 / 8 Plus", "Samsung Galaxy S9", "iPad Pro (3rd generation)", "Huawei P20"],
                '2019': ["Nokia 9 PureView", "iPhone 11", "Samsung Galaxy S10", "iPad Air (3rd generation)", "Google Pixel 4"],
                '2020': ["Nokia 5.3", "iPhone SE (2nd generation)", "Samsung Galaxy S20", "iPad Pro (4th generation)", "OnePlus 8"],
                '2021': ["Nokia G20", "iPhone 12", "Samsung Galaxy S21", "iPad Pro (5th generation)", "Google Pixel 5"],
                '2022': ["Nokia G50", "iPhone 13", "Samsung Galaxy S22", "iPad Air (5th generation)", "Huawei P40"],
                '2023': ["Nokia X20", "iPhone 14", "Samsung Galaxy S23", "iPad (10th generation)", "OnePlus 10"]
                }
                indonesia_devices = {
                '2010': ["BlackBerry Bold 9780", "iPhone 4", "Samsung Galaxy S", "iPad"],
                '2011': ["BlackBerry Torch 9810", "iPhone 4S", "Samsung Galaxy S II", "iPad 2"],
                '2012': ["BlackBerry Bold 9900", "iPhone 5", "Samsung Galaxy S III", "iPad 3", "Google Nexus 7"],
                '2013': ["BlackBerry Z10", "iPhone 5S", "Samsung Galaxy S4", "iPad Air", "Sony Xperia Z"],
                '2014': ["BlackBerry Passport", "iPhone 6 / 6 Plus", "Samsung Galaxy S5", "iPad Air 2", "LG G3"],
                '2015': ["BlackBerry Priv", "iPhone 6S / 6S Plus", "Samsung Galaxy S6", "iPad Pro", "Huawei P8"],
                '2016': ["Samsung Galaxy J7 Prime", "iPhone SE", "Samsung Galaxy S7", "iPad Pro (9.7-inch)", "Google Pixel"],
                '2017': ["Samsung Galaxy J7 Pro", "iPhone 7 / 7 Plus", "Samsung Galaxy S8", "iPad (5th generation)", "Xiaomi Redmi Note 4"],
                '2018': ["Samsung Galaxy A8", "iPhone 8 / 8 Plus", "Samsung Galaxy S9", "iPad Pro (3rd generation)", "Oppo F9"],
                '2019': ["Samsung Galaxy A50", "iPhone 11", "Samsung Galaxy S10", "iPad Air (3rd generation)", "Xiaomi Redmi Note 7"],
                '2020': ["Samsung Galaxy A51", "iPhone SE (2nd generation)", "Samsung Galaxy S20", "iPad Pro (4th generation)", "Realme 6"],
                '2021': ["Samsung Galaxy A52", "iPhone 12", "Samsung Galaxy S21", "iPad Pro (5th generation)", "Xiaomi Redmi Note 10"],
                '2022': ["Samsung Galaxy A53", "iPhone 13", "Samsung Galaxy S22", "iPad Air (5th generation)", "Oppo Reno 7"],
                '2023': ["Samsung Galaxy A54", "iPhone 14", "Samsung Galaxy S23", "iPad (10th generation)", "Realme 9"]
                }
                iran_devices = {
                '2010': ["Samsung Galaxy S", "iPhone 4", "iPad", "Sony Ericsson Xperia X10"],
                '2011': ["Samsung Galaxy S II", "iPhone 4S", "iPad 2", "HTC Sensation"],
                '2012': ["Samsung Galaxy S III", "iPhone 5", "iPad 3", "Sony Xperia S"],
                '2013': ["Samsung Galaxy S4", "iPhone 5S", "iPad Air", "HTC One"],
                '2014': ["Samsung Galaxy Note 3", "iPhone 6 / 6 Plus", "iPad Air 2", "Sony Xperia Z3"],
                '2015': ["Samsung Galaxy S6", "iPhone 6S / 6S Plus", "iPad Pro", "Huawei P8"],
                '2016': ["Samsung Galaxy S7", "iPhone SE", "iPad Pro (9.7-inch)", "LG G5"],
                '2017': ["Samsung Galaxy S8", "iPhone 7 / 7 Plus", "iPad (5th generation)", "Google Pixel"],
                '2018': ["Samsung Galaxy S9", "iPhone 8 / 8 Plus", "iPad Pro (3rd generation)", "Huawei P20"],
                '2019': ["Samsung Galaxy S10", "iPhone 11", "iPad Air (3rd generation)", "Xiaomi Mi 9"],
                '2020': ["Samsung Galaxy S20", "iPhone SE (2nd generation)", "iPad Pro (4th generation)", "Realme 6"],
                '2021': ["Samsung Galaxy S21", "iPhone 12", "iPad Pro (5th generation)", "Xiaomi Redmi Note 10"],
                '2022': ["Samsung Galaxy S22", "iPhone 13", "iPad Air (5th generation)", "Oppo Find X4 Pro"],
                '2023': ["Samsung Galaxy S23", "iPhone 14", "iPad (10th generation)", "OnePlus 10"]
                }
                egypt_devices = {
                '2010': ["iPhone 4", "Samsung Galaxy S", "iPad", "Nokia N8"],
                '2011': ["iPhone 4S", "Samsung Galaxy S II", "iPad 2", "HTC Sensation"],
                '2012': ["iPhone 5", "Samsung Galaxy S III", "iPad 3", "Sony Xperia S"],
                '2013': ["iPhone 5S", "Samsung Galaxy S4", "iPad Air", "HTC One"],
                '2014': ["iPhone 6 / 6 Plus", "Samsung Galaxy Note 3", "iPad Air 2", "Sony Xperia Z3"],
                '2015': ["iPhone 6S / 6S Plus", "Samsung Galaxy S6", "iPad Pro", "Huawei P8"],
                '2016': ["iPhone SE", "Samsung Galaxy S7", "iPad Pro (9.7-inch)", "LG G5"],
                '2017': ["iPhone 7 / 7 Plus", "Samsung Galaxy S8", "iPad (5th generation)", "Google Pixel"],
                '2018': ["iPhone 8 / 8 Plus", "Samsung Galaxy S9", "iPad Pro (3rd generation)", "Huawei P20"],
                '2019': ["iPhone 11", "Samsung Galaxy S10", "iPad Air (3rd generation)", "Xiaomi Mi 9"],
                '2020': ["iPhone SE (2nd generation)", "Samsung Galaxy S20", "iPad Pro (4th generation)", "Realme 6"],
                '2021': ["iPhone 12", "Samsung Galaxy S21", "iPad Pro (5th generation)", "Xiaomi Redmi Note 10"],
                '2022': ["iPhone 13", "Samsung Galaxy S22", "iPad Air (5th generation)", "Oppo Find X4 Pro"],
                '2023': ["iPhone 14", "Samsung Galaxy S23", "iPad (10th generation)", "OnePlus 10"]
                }
                afghanistan_devices = {
                '2010': ["iPhone 4", "Samsung Galaxy S", "iPad", "Nokia N8"],
                '2011': ["iPhone 4S", "Samsung Galaxy S II", "iPad 2", "HTC Sensation"],
                '2012': ["iPhone 5", "Samsung Galaxy S III", "iPad 3", "Sony Xperia S"],
                '2013': ["iPhone 5S", "Samsung Galaxy S4", "iPad Air", "HTC One"],
                '2014': ["iPhone 6 / 6 Plus", "Samsung Galaxy Note 3", "iPad Air 2", "Sony Xperia Z3"],
                '2015': ["iPhone 6S / 6S Plus", "Samsung Galaxy S6", "iPad Pro", "Huawei P8"],
                '2016': ["iPhone SE", "Samsung Galaxy S7", "iPad Pro (9.7-inch)", "LG G5"],
                '2017': ["iPhone 7 / 7 Plus", "Samsung Galaxy S8", "iPad (5th generation)", "Google Pixel"],
                '2018': ["iPhone 8 / 8 Plus", "Samsung Galaxy S9", "iPad Pro (3rd generation)", "Huawei P20"],
                '2019': ["iPhone 11", "Samsung Galaxy S10", "iPad Air (3rd generation)", "Xiaomi Mi 9"],
                '2020': ["iPhone SE (2nd generation)", "Samsung Galaxy S20", "iPad Pro (4th generation)", "Realme 6"],
                '2021': ["iPhone 12", "Samsung Galaxy S21", "iPad Pro (5th generation)", "Xiaomi Redmi Note 10"],
                '2022': ["iPhone 13", "Samsung Galaxy S22", "iPad Air (5th generation)", "Oppo Find X4 Pro"],
                '2023': ["iPhone 14", "Samsung Galaxy S23", "iPad (10th generation)", "OnePlus 10"]
                }
                philippines_devices = {
                '2010': ["iPhone 4", "Samsung Galaxy S", "iPad", "Nokia N8"],
                '2011': ["iPhone 4S", "Samsung Galaxy S II", "iPad 2", "HTC Sensation"],
                '2012': ["iPhone 5", "Samsung Galaxy S III", "iPad 3", "Sony Xperia S"],
                '2013': ["iPhone 5S", "Samsung Galaxy S4", "iPad Air", "HTC One"],
                '2014': ["iPhone 6 / 6 Plus", "Samsung Galaxy Note 3", "iPad Air 2", "Sony Xperia Z3"],
                '2015': ["iPhone 6S / 6S Plus", "Samsung Galaxy S6", "iPad Pro", "Huawei P8"],
                '2016': ["iPhone SE", "Samsung Galaxy S7", "iPad Pro (9.7-inch)", "LG G5"],
                '2017': ["iPhone 7 / 7 Plus", "Samsung Galaxy S8", "iPad (5th generation)", "Google Pixel"],
                '2018': ["iPhone 8 / 8 Plus", "Samsung Galaxy S9", "iPad Pro (3rd generation)", "Huawei P20"],
                '2019': ["iPhone 11", "Samsung Galaxy S10", "iPad Air (3rd generation)", "Xiaomi Mi 9"],
                '2020': ["iPhone SE (2nd generation)", "Samsung Galaxy S20", "iPad Pro (4th generation)", "Realme 6"],
                '2021': ["iPhone 12", "Samsung Galaxy S21", "iPad Pro (5th generation)", "Xiaomi Redmi Note 10"],
                '2022': ["iPhone 13", "Samsung Galaxy S22", "iPad Air (5th generation)", "Oppo Find X4 Pro"],
                '2023': ["iPhone 14", "Samsung Galaxy S23", "iPad (10th generation)", "OnePlus 10"]
                }
                if country_clan == 'United State of America':
                    country = United_State_of_America
                elif country_clan == 'Canada':
                   country = Canada
                elif country_clan == 'India':
                   country = india_devices
                elif country_clan == 'Japan':
                   country = Japan
                elif country_clan == 'Bangladesh':
                   country = Bangladesh
                elif country_clan == 'United Kingdom':
                   country = uk_devices
                elif country_clan == 'France':
                   country = france_devices
                elif country_clan == 'Finland':
                   country = finland_devices
                elif country_clan == 'Indonesia':
                   country = indonesia_devices
                elif country_clan == 'Iran':
                   country = iran_devices
                elif country_clan == 'Egypt':
                   country = egypt_devices
                elif country_clan == 'Afghanistan':
                   country = afghanistan_devices
                elif country_clan == 'P`hilippines':
                   country = philippines_devices
                else:
                   country = International
                update.message.reply_text(f"Fetching [{tag}] Devices!")
                if user_input in country:
                        # If the input is a key, choose a random value from its list
                        random_value = random.choice(country[user_input])
                        # Find the index of the current key
                        key_index = list(country.keys()).index(user_input)
                        # Fetch the next key (if available) and choose a random value
                        if key_index + 1 < len(country):
                            next_key = list(country.keys())[key_index + 1]
                            random_next_value1 = random.choice(country[next_key])
                            if key_index + 2 < len(country):
                             next_key = list(country.keys())[key_index + 2]
                             random_next_value2 = random.choice(country[next_key])
                             if key_index + 3 < len(country):
                              next_key = list(country.keys())[key_index + 3]
                              random_next_value3 = random.choice(country[next_key])
                              if key_index + 4 < len(country):
                               next_key = list(country.keys())[key_index + 4]
                               random_next_value4 = random.choice(country[next_key])
                               if key_index + 5 < len(country):
                                next_key = list(country.keys())[key_index + 5]
                                random_next_value5 = random.choice(country[next_key])
                                if key_index + 6 < len(country):
                                 next_key = list(country.keys())[key_index + 6]
                                 random_next_value6 = random.choice(country[next_key])
                                 if key_index + 7 < len(country):
                                  next_key = list(country.keys())[key_index + 7]
                                  random_next_value7 = random.choice(country[next_key])
                                 if key_index + 8 < len(country):
                                  next_key = list(country.keys())[key_index + 8]
                                  random_next_value8 = random.choice(country[next_key])
                                  if key_index + 9 < len(country):
                                   next_key = list(country.keys())[key_index + 9]
                                   random_next_value9 = random.choice(country[next_key])
                                   if key_index + 10 < len(country):
                                    next_key = list(country.keys())[key_index + 10]
                                    random_next_value10 = random.choice(country[next_key])
                                    if key_index + 11 < len(country):
                                     next_key = list(country.keys())[key_index + 11]
                                     random_next_value11 = random.choice(country[next_key])
                                     if key_index + 12 < len(country):
                                      next_key = list(country.keys())[key_index + 12]
                                      random_next_value12 = random.choice(country[next_key])
                                     if key_index + 13 < len(country):
                                       next_key = list(country.keys())[key_index + 13]
                                       random_next_value13 = random.choice(country[next_key])  
                
                        if user_input == '2010':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3},\n {random_next_value4},\n {random_next_value5},\n {random_next_value6},\n {random_next_value7},\n{random_next_value8},\n{random_next_value9},\n{random_next_value10},\n{random_next_value11},\n{random_next_value12},\n{random_next_value13}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2011':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3},\n {random_next_value4},\n {random_next_value5},\n {random_next_value6},\n {random_next_value7},\n{random_next_value8},\n{random_next_value9},\n{random_next_value10},\n{random_next_value11},\n{random_next_value12}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2012':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3},\n {random_next_value4},\n {random_next_value5},\n {random_next_value6},\n {random_next_value7},\n{random_next_value8},\n{random_next_value9},\n{random_next_value10},\n{random_next_value11}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2013':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3},\n {random_next_value4},\n {random_next_value5},\n {random_next_value6},\n {random_next_value7},\n{random_next_value8},\n{random_next_value9},\n{random_next_value10}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2014':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3},\n {random_next_value4},\n {random_next_value5},\n {random_next_value6},\n {random_next_value7},\n{random_next_value8},\n{random_next_value9}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2015':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3},\n {random_next_value4},\n {random_next_value5},\n {random_next_value6},\n {random_next_value7},\n{random_next_value8}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2016':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3},\n {random_next_value4},\n {random_next_value5},\n {random_next_value6},\n {random_next_value7}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2017':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3},\n {random_next_value4},\n {random_next_value5},\n {random_next_value6}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2018':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3},\n {random_next_value4},\n {random_next_value5}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2019':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3},\n {random_next_value4}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2020':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2},\n {random_next_value3}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2021':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1},\n {random_next_value2}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2022':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value},\n {random_next_value1}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        elif user_input == '2023':
                          update.message.reply_text(f"✨🌟💫            ✨🌟💫                   ✨🌟💫\n📱Devices of your account Tag:#️⃣{tag}:\n {random_value}\n✨🌟💫            ✨🌟💫                   ✨🌟💫")
                        else:
                          update.message.reply_text("✨🌟💫            ✨🌟💫                   ✨🌟💫\nEnter the valid year between 2010 - 2023\n✨🌟💫            ✨🌟💫                   ✨🌟💫")      
            else:
               update.message.reply_text("Invalid Tag!")
def tag(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:    
        if update.message.text == '/tag':
         update.message.reply_text("Enter a Player Tag with Proper Syntax like /tag #8HDI293HD")  
        else:
          input = update.message.text.split(' ')
          tag = input[1].upper()
          tag_without_hash = tag.replace('#','')

          if tag == '':
             update.message.reply_text("Enter player tag, remove one space because you are giving two Spaces ")
          else:   
            update.message.reply_text(f"🤖Tag #{tag_without_hash} is Collected✅")
            #basic details
            cos1_url_name = f"https://www.clashofstats.com/players/{tag_without_hash}/summary"
            response = requests.get(cos1_url_name, proxies={'http': proxy_url, 'https': proxy_url})
            html_content = response.text
            if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
              soup = BeautifulSoup(html_content, 'html.parser')
            # Find and extract the latest date from the HTML content
              Current_name_section = soup.find('h1', class_='display-2')
              body_elements = soup.find_all('span', class_='num-val')
              body2_elements = soup.find_all('span', class_='body-2')
              #body 1
              if Current_name_section:
                Current_name= Current_name_section.text
              else:
                  Current_name = ("Invalid Player tag\nBanned player!")
              if len(body_elements) >=5:
                  TH_level = body_elements[0].text.strip()   
                  BH_level = body_elements[1].text.strip()  
                  Clan_location_level = body_elements[2].text.strip()   
                  Clan_name = body_elements[3].text.strip()  
                  Rank = body_elements[4].text.strip()
              elif len(body_elements) ==4:
                  TH_level = body_elements[0].text.strip()   
                  BH_level = ("Not open Yet")
                  Clan_location_level = body_elements[1].text.strip()   
                  Clan_name = body_elements[2].text.strip()  
                  Rank = body_elements[3].text.strip()
              elif len(body_elements) ==3:
                  TH_level = body_elements[0].text.strip()   
                  BH_level = body_elements[1].text.strip()  
                  Clan_location_level = body_elements[2].text.strip()   
                  Clan_name = ("Not in a clan")
                  Rank = ("None")
              elif len(body_elements) ==2:
                  TH_level = body_elements[0].text.strip()   
                  BH_level = ("Not open Yet")
                  Clan_location_level = body_elements[1].text.strip()   
                  Clan_name = ("Not in a clan")
                  Rank = ("None!")
              else:
                 TH_level = ("Not Found")
                 BH_level = ("Not Found")
                 Clan_location_level = ("Not Found")
                 Clan_name = ("Not Found")
                 Rank = ("Not Found")
                
                  #body 2
              if len(body2_elements) >=10:
                  Exp_level = body2_elements[0].text.strip()  
                  war_star = body2_elements[1].text.strip()  
                  TH_trophies = body2_elements[2].text.strip()
                  Reached_trophies = body2_elements[3].text.strip()
                  BH_trophies = body2_elements[4].text.strip() 
              elif len(body2_elements) ==9:
                  Exp_level = body2_elements[0].text.strip()  
                  war_star = body2_elements[1].text.strip()  
                  TH_trophies = body2_elements[2].text.strip()
                  Reached_trophies = ("None!")
                  BH_trophies = body2_elements[3].text.strip() 
              else:
                  Exp_level = ("Not Found")
                  war_star = ("Not Found")
                  TH_trophies = ("Not Found")
                  Reached_trophies = ("Not Found")
                  BH_trophies = ("Not Found")
              #Location
              coc_url_location = f"https://www.clashofstats.com/players/{tag_without_hash}/history/"
              response = requests.get(coc_url_location, proxies={'http': proxy_url, 'https': proxy_url})
              if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                span_element = soup.find('span', class_='text--secondary caption')
                if span_element:
                  clan_tag = span_element.text.strip()
                  clan_tag_ = clan_tag.replace('#', '')
                else:
                  clan_tag_ = "NA"
              else:
                 clan_tag_ = ("Not Found!")
              cos_url_loaction1 = f"https://www.clashofstats.com/clans/{clan_tag_}/history/past-members?filter=%23{tag_without_hash}"  # Replace "URL_HERE" with the actual URL containing the HTML element
              if response.status_code == 200:
                  response = requests.get(cos_url_loaction1, proxies={'http': proxy_url, 'https': proxy_url})
                  soup = BeautifulSoup(response.text, 'html.parser')
                  span_elements = soup.find_all('span', class_='num-val')
                  if len(span_elements) >= 3:
                      country = span_elements[2].text.strip()
                  else:
                   country = ("None!")
              else:
                 country = ("None!")

              #Last PLayed
              url = f"https://fwa.chocolateclash.com/cc_n/member.php?tag={tag_without_hash}&anyways"
              print(url)
              response = requests.get(url, proxies={'http': proxy_url, 'https': proxy_url})
              html_content = response.text
              if response.status_code == 200:           
                      # Parse the HTML content with BeautifulSoup
                  soup = BeautifulSoup(html_content, 'html.parser')
              
                  date_element = soup.find('a', href='#')
                  if date_element:  
                      first_date = date_element.text.strip()
                  else:
                      first_date = ("Not Found!")
                         
                      #war_inspect_id
                  url1 = f"https://fwa.chocolateclash.com/cc_n/member.php?tag={tag_without_hash}&rlim=30&slim=5110"
                  
                  if response == requests.get(url, proxies={'http': proxy_url, 'https': proxy_url}):
                   response = requests.get(url1, proxies={'http': proxy_url, 'https': proxy_url})
                  elif response == requests.get(url, proxies={'http': proxy_url, 'https': proxy_url}):
                   response = requests.get(url, proxies={'http': proxy_url, 'https': proxy_url})
                  response.raise_for_status()
                  soup = BeautifulSoup(response.content, 'html.parser')
                  tables = soup.find_all('table')
                  # Check if there is a second table
                  if len(tables) >= 2:
                      second_table = tables[1]
                      
                      href_links = [a['href'] for a in second_table.find_all('a', href=True)] if second_table else []
                      if len(href_links) >= 3:
                        last_third_link = href_links[-3]
                        print("-3")
                        if last_third_link[0:8] == 'clan.php':
                            last_third_link = href_links[-4]
                            print("-4")
                        elif len(href_links) == 0:
                         last_third_link = ("Not Found!")
                      else:
                         print("Not Found, Invalid Tag")
                      
                         #Previous Name
                      if len(tables) == 0:
                       print("Previos Name: Not Found")   
                      elif len(href_links) ==0:
                         player_name1 = ("Not Found!")
                      else:
                       url_war_inspect =  f"https://fwa.chocolateclash.com/cc_n/{last_third_link}"
                       print(url_war_inspect)
                       response = requests.get(url_war_inspect, proxies={'http': proxy_url, 'https': proxy_url})
                      if response.status_code == 200:
                          # Parsing the HTML content
                          soup = BeautifulSoup(response.text, 'html.parser')
                          td_elements = soup.find_all('td')
                          for td_element in td_elements:
                              if tag in td_element.get_text():
                                  player_name1 = td_element.get_text().split(f' (#{tag_without_hash})')[0].strip()
                      else:   
                          print(f"Failed to fetch data. Status code: {response.status_code}")
                  else: 
                      print("Not find the 2nd table")
                      last_third_link = "Not Found!"
              else: 
                      first_date = ("Not Found!")
                      print(last_third_link)
                      player_name1 = ("None!")
                
              if len(tag_without_hash) == 9:
                first_letter = tag_without_hash[0]
                if first_letter == '2':
                    Creation_date = "Mid-Late 2015"
                elif first_letter == '8':
                    Creation_date = "Early-Mid 2015"
                elif first_letter == '9':
                    Creation_date = "Early-Mid 2016"
                elif first_letter == 'P':
                    Creation_date = "Late-2016 2017"
                elif first_letter == 'Y':
                    Creation_date = "Late-2017 2018"
                elif first_letter == 'L':
                    Creation_date = "Late-2018 2019"
                elif first_letter == 'Q':
                    Creation_date = "Late-2020 2021"
                else:
                    Creation_date = "Invalid Tag!"
              elif len(tag_without_hash) == 8:
                  first_letter = tag_without_hash[0]
                  if first_letter == 'Q':
                      Creation_date = "Late 2013"
                  elif first_letter == 'G':
                      Creation_date = "Early-Mid 2013"
                  elif first_letter == 'R':
                      Creation_date = "Summer 2013"
                  elif first_letter == 'v':
                      Creation_date = "Late 2014"
                  elif first_letter == 'P':
                      Creation_date = "Early-Middle 2014"
                  elif first_letter == '9':
                      Creation_date = "Middle 2014"
                  elif first_letter == '8':
                      Creation_date = "Summer 2014"
                  elif first_letter == 'J':
                      Creation_date = "Late-2014 2015"
                  else:
                      Creation_date = "Invalid Tag"
              elif len(tag_without_hash) == 7:
                  first_letter = tag_without_hash[0]
                  if first_letter == 'U':
                      Creation_date = "December 2012"
                  elif first_letter == '2':
                      Creation_date = "December 2012"
                  elif first_letter == 'L':
                      Creation_date = "December 2012"
                  else:
                      Creation_date = "Early 2013"
              elif len(tag_without_hash) == 6:
                  first_letter = tag_without_hash[0]
                  if first_letter == 'U':
                      Creation_date = "August 2012"
                  elif first_letter:
                      Creation_date = "October 2012"
                  else:
                      Creation_date = "Summer-Autumn 2012"
              elif len(tag_without_hash) < 6:
                   Creation_date = "Invalid player tag" 
              else:
                  Creation_date = "Invalid player tag" 
            else:
               update.message.reply_text("Invalid Tag")   
          if __name__ == "__main__":
            if response.status_code == 200:
              update.message.reply_text(f"""✨🌟💫            ✨🌟💫                   ✨🌟💫
👤𝗡𝗮𝗺𝗲: {Current_name}\n👥𝐂𝐥𝐚𝐧: {Clan_name}\n📈𝐑𝐚𝐧𝐤: {Rank}\n🌐𝐂𝐥𝐚𝐧 𝐋𝐨𝐜𝐚𝐭𝐢𝐨𝐧: {Clan_location_level}\n
💥𝐋𝐞𝐯𝐞𝐥: {Exp_level}\n🏡𝐓𝐨𝐰𝐧 𝐇𝐚𝐥𝐥 𝐥𝐞𝐯𝐞𝐥: {TH_level}\n🏆𝐓𝐫𝐨𝐩𝐡𝐢𝐞𝐬: {TH_trophies}\n🏁𝐑𝐞𝐚𝐜𝐡𝐞𝐝 𝐓𝐫𝐨𝐩𝐡𝐢𝐞𝐬: {Reached_trophies}\n⭐️𝐖𝐚𝐫 𝐒𝐭𝐚𝐫𝐬: {war_star}\n
🎃𝐁𝐮𝐢𝐥𝐝𝐞𝐫 𝐇𝐚𝐥𝐥 𝐥𝐞𝐯𝐞𝐥: {BH_level}\n🏆𝐁𝐇 𝐓𝐫𝐨𝐩𝐡𝐢𝐞𝐬: {BH_trophies}\n
🎌Country: {country}\n✯𝐂𝐫𝐞𝐚𝐭𝐢𝐨𝐧 𝐃𝐚𝐭𝐞: {Creation_date}\n🕘𝐋𝐚𝐬𝐭 𝐏𝐥𝐚𝐲𝐞𝐝:\n>> {first_date[0:11]} | {first_date[10:19]} EDT\n✨𝐏𝐫𝐞𝐯𝐢𝐨𝐮𝐬 𝐍𝐚𝐦𝐞: {player_name1}
✨🌟💫            ✨🌟💫                   ✨🌟💫""")
            else:
               update.message.reply_text("Enter a Valid Tag!")
def download_command(update, context):
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The file is being ready..")
        context.bot.send_message(chat_id=update.effective_chat.id, text="The file is downloading....")
        context.bot.send_document(chat_id=update.effective_chat.id, document=open('user_input/output.pdf', 'rb'))
        print("pdf sended!")
def Guide_command(update, context):
    user_id = update.effective_user.id
    if user_id not in user_auth_status:  # If the user is already authenticated
        update.message.reply_text("Please authenticate first by entering the password.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The file is being ready..")
        context.bot.send_document(chat_id=update.effective_chat.id, document=open('Guide.doc', 'rb'))
        print("pdf sended!")

def error_handler(update: Update, context: CallbackContext):
    """Log any errors that occur."""
    logging.error(f'Error: {context.error}')
    
def main():
    # Create an updater and dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatch = updater.dispatcher
    dispatch.add_handler(telegram.ext.CommandHandler('start', start))
    dispatch.add_handler(MessageHandler(Filters.text & ~Filters.command, password_input))
    dispatch.add_handler(telegram.ext.CommandHandler('add_password', add_password))
    dispatch.add_handler(telegram.ext.CommandHandler('delete_password', delete_password))
    dispatch.add_handler(telegram.ext.CommandHandler('user_auth_status', user_auth_status_command))
    dispatch.add_handler(telegram.ext.CommandHandler('valid_passwords', valid_passwords_command))
    dispatch.add_handler(telegram.ext.CommandHandler('Report_bug', Report_bug_command))
    dispatch.add_handler(telegram.ext.CommandHandler('Report_bug_check', Report_bug_check_command))
    dispatch.add_handler(telegram.ext.CommandHandler('Report_bug_delete', Report_bug_delete_command))
    dispatch.add_handler(telegram.ext.CommandHandler('Suggestion', Suggestion_command))
    dispatch.add_handler(telegram.ext.CommandHandler('Suggestion_check', Suggestion_check_command))
    dispatch.add_handler(telegram.ext.CommandHandler('Suggestion_reply', Suggestion_reply_command))
    dispatch.add_handler(telegram.ext.CommandHandler('Suggestion_check_reply', Suggestion_check_reply_command))
    dispatch.add_handler(telegram.ext.CommandHandler('user_auth_status_delete', user_auth_status_delete_command))
    send_update_handler = CommandHandler('send_update', send_update)
    dispatch.add_handler(send_update_handler)
    dispatch.add_handler(telegram.ext.CommandHandler('help', help_command))
    dispatch.add_handler(telegram.ext.CommandHandler('help_owner', help_owner_command))
    dispatch.add_handler(telegram.ext.CommandHandler('receipt', receipt))
    dispatch.add_handler(telegram.ext.CommandHandler('Bypass_receipt', Bypass_receipt))
    dispatch.add_handler(telegram.ext.CommandHandler('generate_receipt', generate_receipt))
    dispatch.add_handler(telegram.ext.CommandHandler('Google_receipt', Google_receipt))
    dispatch.add_handler(telegram.ext.CommandHandler('Apple_receipt', Apple_receipt))
    dispatch.add_handler(telegram.ext.CommandHandler('Apple_receipt_1', Apple_receipt_1))
    dispatch.add_handler(telegram.ext.CommandHandler('Apple_receipt_2', Apple_receipt_2))
    dispatch.add_handler(telegram.ext.CommandHandler('download', download_command))
    dispatch.add_handler(telegram.ext.CommandHandler('data_apple1', data_apple1))
    dispatch.add_handler(telegram.ext.CommandHandler('data_apple2', data_apple2))
    dispatch.add_handler(telegram.ext.CommandHandler('data_google', data_google))
    dispatch.add_handler(telegram.ext.CommandHandler('device', device))
    dispatch.add_handler(telegram.ext.CommandHandler('generate_devices', generate_devices))
    dispatch.add_handler(telegram.ext.CommandHandler('Guide', Guide_command))
    dispatch.add_handler(telegram.ext.CommandHandler('tag', tag))
    dispatch.add_error_handler(error_handler)
    updater.start_polling()
    logger.info("Bot started..")
    updater.idle()
    
if __name__=='__main__':
    main()
    app.run(port=443)
