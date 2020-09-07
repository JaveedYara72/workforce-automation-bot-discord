import discord
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader


# Manual Import
import credentials as CREDENTIALS


file_loader = FileSystemLoader('templates')
env = Environment(loader = file_loader)


async def Email_Project_Registration(reciever_email, name):

	subject = "Project Registration Completed."

	message = MIMEMultipart()
	message["Subject"] = subject
	message["From"] = CREDENTIALS.sender_email
	message["To"] = reciever_email

	template = env.get_template('project_registration.html')

	text = template.render(name = name)

	part1 = MIMEText(text,'html')

	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
	    server.login(CREDENTIALS.sender_email, CREDENTIALS.password)
	    server.sendmail(CREDENTIALS.sender_email,reciever_email, message.as_string())



async def Email_Project_Confirmation(reciever_email, name, project_name):

	subject = "Project Registration Confirmation"

	message = MIMEMultipart()
	message["Subject"] = subject
	message["From"] = CREDENTIALS.sender_email
	message["To"] = reciever_email

	template = env.get_template('project_confirmation.txt')

	text = template.render(name = name, project_name = project_name)

	part1 = MIMEText(text,'html')

	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
	    server.login(CREDENTIALS.sender_email, CREDENTIALS.password)
	    server.sendmail(CREDENTIALS.sender_email,reciever_email, message.as_string())


async def Email_Community(reciever_email, name):

	subject = "Registration Community"

	message = MIMEMultipart()
	message["Subject"] = subject
	message["From"] = CREDENTIALS.sender_email
	message["To"] = reciever_email

	template = env.get_template('community.txt')

	text = template.render(name = name)

	part1 = MIMEText(text,'html')

	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
	    server.login(CREDENTIALS.sender_email, CREDENTIALS.password)
	    server.sendmail(CREDENTIALS.sender_email,reciever_email, message.as_string())


async def Email_Career_At_Koders(reciever_email, name):

	subject = "Career At Koders"

	message = MIMEMultipart()
	message["Subject"] = subject
	message["From"] = CREDENTIALS.sender_email
	message["To"] = reciever_email

	template = env.get_template('carrer.txt')

	text = template.render(name = name)

	part1 = MIMEText(text,'html')

	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
	    server.login(CREDENTIALS.sender_email, CREDENTIALS.password)
	    server.sendmail(CREDENTIALS.sender_email,reciever_email, message.as_string())


async def Email_Internship_Confirmation(reciever_email, name):

	subject = "Registration Community"

	message = MIMEMultipart()
	message["Subject"] = subject
	message["From"] = CREDENTIALS.sender_email
	message["To"] = reciever_email

	template = env.get_template('internship_confirmation.txt')

	text = template.render(name = name)

	part1 = MIMEText(text,'html')

	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
	    server.login(CREDENTIALS.sender_email, CREDENTIALS.password)
	    server.sendmail(CREDENTIALS.sender_email,reciever_email, message.as_string())	    



async def Email_New_Functionalities(reciever_email, name):

	subject = "New Functionalities"

	message = MIMEMultipart()
	message["Subject"] = subject
	message["From"] = CREDENTIALS.sender_email
	message["To"] = reciever_email

	template = env.get_template('new_functionalities.txt')

	text = template.render(name = name)

	part1 = MIMEText(text,'html')

	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
	    server.login(CREDENTIALS.sender_email, CREDENTIALS.password)
	    server.sendmail(CREDENTIALS.sender_email,reciever_email, message.as_string())