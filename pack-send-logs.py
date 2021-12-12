from datetime import datetime
import os
import re
import sys

from zipfile import ZipFile

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from configparser import ConfigParser

config = ConfigParser()
config.read('voice-assistant.ini')

files_count = 0
zipfilename = "/tmp/voice-assisstant-logs_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".zip"
with ZipFile(zipfilename, 'w') as zf:
    for dirname, subdirs, filenames in os.walk('/tmp/'):
        for filename in filenames:
            match = re.search(r"voice-assistant.log.\d+", filename)
            if match:
                fpath = os.path.join(dirname, filename)
                zf.write(fpath, filename)
                os.remove(fpath)
                files_count += 1

print("The {} files were zipped.".format(files_count))
if files_count == 0:
    os.remove(zipfilename)
    sys.exit(0)

subject = "VoiceAssistant logs"
body = "VoiceAssistan logs"

sender = config.get('email', 'sender')
recipient = config.get('email', 'recipient')
password = config.get('email', 'password')

message = MIMEMultipart()
message["From"] = sender
message["To"] = recipient
message["Subject"] = subject
message["Bcc"] = recipient


with open(zipfilename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    
encoders.encode_base64(part)

part.add_header("Content-Disposition", "attachment; filename={}".format(zipfilename))

message.attach(part)
text = message.as_string()
 
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.mail.ru", 465, context=context) as server:
    server.login("voice.assistant", password)
    server.sendmail(sender, recipient, text)
    
os.remove(zipfilename)