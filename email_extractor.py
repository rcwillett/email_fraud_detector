# Import libraries to be used in this script
import sys
import os
import email
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import quopri
import re

path = sys.argv[1]
listing = os.listdir(path)
success = 0
failed = 0
email_content_list = []
for fle in listing:
    try:
        if str.lower(fle[-3:])=="eml":
            email_dict = {}
            fp = open(f'{path}{fle}', 'rb')  # select a specific email file from the list
            name = fp.name # Get file name
            msg = email.parser.BytesParser().parse(fp)
            email_dict['subject'] = msg['Subject']
            email_dict['from'] = msg['From']
            cp = msg.get_content_type()
            if (cp == 'multipart/alternative'):
                html = ''
                y = 0
                while 1:
                    # If we cannot get the payload, it means we hit the end:
                    try:
                        pl = msg.get_payload(y)
                    except: break
                    html += pl.as_string()
                    y += 1
            elif (cp == 'text/html'):
                html = msg.get_payload()
            if html.isascii():
                decoded = quopri.decodestring(html)
                soup = BeautifulSoup(decoded, features="html.parser")
                links = soup.find_all('a', href=True)
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
        failed += 1
df = pd.DataFrame(data=email_content_list, columns=['from', 'subject', 'content'])
df.to_csv(sys.argv[2], index=False)
print(f'Successfully processed: {success}\nFailed to process: {failed}')