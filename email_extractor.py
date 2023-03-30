# Import system libraries 
import sys
import os

# Import default libraries for parsing and string manipulation
import re
import email
import quopri

# Import standard data science libraries
import pandas as pd
import numpy as np

# Import html parsing library
from bs4 import BeautifulSoup

# Set path variable to first input argument
path = sys.argv[1]

# Get all files in path
listing = os.listdir(path)

# Initialize success and fail count for parsing
success = 0
failed = 0

# Initialize list to store email data
email_content_list = []

# Iterate over files in directory
for fle in listing:
    try:
        # Check if file has the .eml extension otherwise ignore
        if str.lower(fle[-3:])=="eml":
            # Set up dictionary to record email details
            email_dict = {}
            # Initialize email content as empty string
            content = ''
            # Open email file
            fp = open(f'{path}{fle}', 'rb')
            # Parse the email file using the email file parser
            msg = email.parser.BytesParser().parse(fp)
            # Get basic information from email (subject, to, from)
            email_dict['subject'] = msg['Subject']
            email_dict['from'] = msg['From']
            email_dict['to'] = msg['To']
            # Get content type of email
            eml_content_format = msg.get_content_type()
            # Check if email content multipart/alternative
            if (eml_content_format == 'multipart/alternative'):
                # initialize part count variable
                part = 0
                # Initialize while loop to iterate over email content parts
                while 1:
                    # If we cannot get the payload, it means we hit the end:
                    try:
                        payload = msg.get_payload(part)
                    except: break
                    content += payload.as_string()
                    part += 1
            # Check if content text/html and get content if so
            elif (eml_content_format == 'text/html'):
                content = msg.get_payload()
            # Check if content plain text and get content if so
            elif (eml_content_format == 'text/plain'):
                content = msg.get_payload()
            # Check if content is ascii format and not empty
            if content.isascii() and content != '':
                # Decodes any quoted-printable encoded characters
                decoded = quopri.decodestring(content)
                # Soupifys any HTML content
                soup = BeautifulSoup(decoded, features="html.parser")
                # Pulls any text content from soupified string
                text = soup.get_text()
                # Removes any "Content-Type" style strings
                text = re.sub('Content\-Type\:.*', '', text)
                text = re.sub('Content\-Transfer\-Encoding:.*', '', text)
                # Removes any newline or tab characters in text
                text = text.replace('\n', ' ').replace('\t', ' ')
                # Removes any non-standard characters from text
                text = re.sub(r'[^a-zA-Z0-9\s\.\,\-\/\\\%\&\$\:]','',text)
                # Removes any "charsetiso." style string from text
                text = re.sub(r'charsetiso.8859.1.*charsetiso.8859.1', '', text)
                # Removes any multiple spaced characters
                text = re.sub(r'\s\s+',' ',text)
                # Removes any starting spaces
                text = re.sub(r'^\s*','',text)
                # Sets email content dict to formatted text
                email_dict['content'] = text
                # Increments success counter
                success += 1
                # Adds email content dict to email content list
                email_content_list.append(email_dict)
            else:
                # Increments fail count (If content not ascii)
                failed += 1
            # Closes opened file
            fp.close()
    except:
        # Increment failed count on failure
        failed += 1

# Create data frame from email content dictionaries
df = pd.DataFrame(data=email_content_list, columns=['from', 'to', 'subject', 'content'])
# Saves data frame to csv file with name as second argument to file
df.to_csv(sys.argv[2], index=False)
# Print number of files successfully processed and number unsuccessfully processed
print(f'Successfully processed: {success}\nFailed to process: {failed}')