import os
import sys
import email
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import quopri
import re
import logging

# Get all files in directory
rootDirs = os.listdir(sys.argv[1])

success = 0
failed = 0
email_content_list = []

# Iterate over all files in directory
for folder in rootDirs:
    if os.path.isdir(f'{sys.argv[1]}/{folder}'):
        userDirs = os.listdir(f'{sys.argv[1]}/{folder}')
        for userDir in userDirs:
            path = f'{sys.argv[1]}/{folder}/{userDir}'
            if os.path.isdir(path) :
                files = os.listdir(path)
                for fle in files:
                    if not os.path.isdir(f'{path}/{fle}'):
                        try:
                            if str.lower(fle[-3:])=="eml":
                                email_dict = {}
                                content = ''
                                fp = open(f'{path}/{fle}', 'rb')  # select a specific email file from the list
                                name = fp.name # Get file name
                                msg = email.parser.BytesParser().parse(fp)
                                email_dict['subject'] = msg['Subject']
                                email_dict['from'] = msg['From']
                                email_dict['to'] = msg['To']
                                cp = msg.get_content_type()
                                if (cp == 'multipart/alternative'):
                                    y = 0
                                    while 1:
                                        # If we cannot get the payload, it means we hit the end:
                                        try:
                                            pl = msg.get_payload(y)
                                        except: break
                                        content += pl.as_string()
                                        y += 1
                                elif (cp == 'text/html'):
                                    content = msg.get_payload()
                                elif (cp == 'text/plain'):
                                    content = msg.get_payload()
                                if content.isascii() and content != '':
                                    decoded = quopri.decodestring(content)
                                    soup = BeautifulSoup(decoded, features="html.parser")
                                    text = soup.get_text()
                                    text = re.sub('Content\-Type\:.*', '', text)
                                    text = re.sub('Content\-Transfer\-Encoding:.*', '', text)
                                    text = text.replace('\n', ' ').replace('\t', ' ')
                                    text = re.sub(r'[^a-zA-Z0-9\s\.\,\-\/\\\%\&\$\:]','',text)
                                    text = re.sub(r'charsetiso.8859.1.*charsetiso.8859.1', '', text)
                                    text = re.sub(r'\s\s+',' ',text)
                                    text = re.sub(r'^\s*','',text)
                                    email_dict['content'] = text
                                    success += 1
                                    email_content_list.append(email_dict)
                                else:
                                    failed += 1
                                fp.close()
                        except:
                            logging.exception('')
                            failed += 1
df = pd.DataFrame(data=email_content_list, columns=['from', 'to', 'subject', 'content'])
df.to_csv(sys.argv[2], index=False)
print(f'Successfully processed: {success}\nFailed to process: {failed}')