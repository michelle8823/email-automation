import smtplib, csv, ssl

from string import Template

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'sample@gmail.com'
CC_ADDRESS = 'someone@gmail.com'

def get_contacts(filename):
    """
    Open csv file containing receiver's names and emails and append them into
    lists
    """
    
    names = []
    emails = []

    with open("sponsor_contacts.csv") as file:
        reader = csv.reader(file)
        # Skip header row
        next(reader)  
        for name, email in reader:
            names.append(name)
            emails.append(email)

    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()

    return Template(template_file_content)

def main():
    names, emails = get_contacts('sponsor_contacts.csv')
    message_template = read_template('message.html')

    # set up the SMTP server
    password = = input("Type your password: ")
    s = smtplib.SMTP(host= 'smtp.gmail.com', port= 587) # change gmail settings to lower security
    s.starttls()
    s.login(MY_ADDRESS, password)

    # Match name and contact together, then send email
    for name, email in zip(names, emails):
        # create message
        msg = MIMEMultipart()       

        # add in contact name to the html message template
        message = message_template.substitute(COMPANY_NAME=name.title())
        
        # Prints message sent 
        print(message)

        # setup the parameters of the message
        msg['From']= MY_ADDRESS
        msg['To']= email
        msg['Cc']= CC_ADDRESS
        msg['Subject']= f"Proposal for {name.title()}"
        
        # Attach html template to message
        msg.attach(MIMEText(message, 'html'))
    
        # Optional attachment of files in email
        filename = "sample.pdf"

        # Open sponsorship proposal PDF file in binary mode
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        msg.attach(part)

        # send the message via the server 
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()
