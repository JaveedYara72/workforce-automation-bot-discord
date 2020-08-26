import discord
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Manual Import
import credentials as CREDENTIALS

async def Email_Project_Registration(reciever_email, name):

	subject = "Project Registration Completed"

	message = MIMEMultipart()
	message["Subject"] = subject
	message["From"] = CREDENTIALS.sender_email
	message["To"] = reciever_email

	# create the plain text and html version of your message

	text = """Hello Koder {}, 
	We're pleased to have you on board with us. Taking a moment to express our gratitude, we're thankful that you registered your project with us. 
	Koders is a kore of fervor developers and we welcome you to our family with our whole heart. Your project has been taken into consideration and our Kore team is working to plan out your project to assess the implementation and execution. 
	Once approved, you will receive a confirmation email from our side and we will kick off with your project. 
	Please understand that due to the crunch of time and our fastidious nature, we only undertake projects after we've thoroughly reviewed it to serve your needs as desired. 
	In the meantime don't forget to check out our past projects<some testimonials, preferably a click here button>. 
	Keep Koding, Keep growing. 
	Regards 
	Team Koders
	""".format(name)

	# turn these into plain/html MIMEText objects

	part1 = MIMEText(text,'plain')


	# Add HTML/plain-text part to MIMEMultipart message
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

	# create the plain text and html version of your message

	text = """Hello Koder {},
	Hope we didn't make you wait long. We're extremely apologetic if a delay arose. 
	It gives us immense pleasure Mr.<name> to convey that after an extensive review of your project by our Kore Team, your project <project name>, <project id>has been selected. 
	One of our representatives will get in touch with you for further advancements. 
	Congratulations! {} is going to be lit. Hold tight as we develop your dream project and turn it into a reality. 
	Keep Koding, Keep growing
	Regards,
	Team Koders.
	""".format(name, project_name)

	# turn these into plain/html MIMEText objects

	part1 = MIMEText(text,'plain')


	# Add HTML/plain-text part to MIMEMultipart message
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

	# create the plain text and html version of your message

	text = f"""Hello Koder {name},
	More than a community, Koders is a family. A family of passionate individuals that don't only Kode, but also develop a pristine relationship with the people who are part of our Koding Family. {name} We welcome you to a community full of vibrance and fruition. 
	Just to give you a brief overview, we suggest you that please go through our <community guidelines>(link to redirect). We strictly abide by them to ensure our family is prosperous and heading towards mutual development. 
	We wish you loads of learning, new experiences, and rest assured, there are a bunch of beautiful humans here to connect with. 
	With utmost compassion. 
	Keep Koding, Keep growing 
	Regards, 
	Team Koders 
	"""

	# turn these into plain/html MIMEText objects

	part1 = MIMEText(text,'plain')

	# Add HTML/plain-text part to MIMEMultipart message
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

	# create the plain text and html version of your message

	text = """Hello Koder {},
	So you think you have got it all to become a Koder? We admire your confidence and are keen to have you on board with us. 
	Koders is a very close-knit organization and we've top-notch standards to ensure efficiency and work ethic in the culture of our company. 
	We firmly believe that you've got it all. Just to double-check, our HR will go through your CV and ensure that your potential is directed to the most suited domain available.
	 The process may take some time and your patience is appreciated
	In the meantime, please make yourself comfortable with <Koders and it's functioning>. 
	We'll get in touch with you real soon! 
	Thank you 
	Keep Koding, Keep growing
	Team Koders.
	""".format(name)

	# turn these into plain/html MIMEText objects

	part1 = MIMEText(text,'plain')

	# Add HTML/plain-text part to MIMEMultipart message
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

	# create the plain text and html version of your message

	text = """Hello, Dear Koder {},
	PFA the appointment letter below. Yes, you have heard it right. We see a lot of potential in you. To mold your potential and channelize it in the right direction, Koders is all that you need. The offer details have been enclosed in the document attached below and we hope that you revert with your decision soon. Koders is waiting to help you sharpen your saw and to ensure that we mutually benefit from each other. Get ready as we introduce you to a work culture that is unmatched. Get ready to become a part of our family which is considerate and will ensure that your fruition is done to its zenith. 
	Wishing you an experience you've never had before with the perfect balance of work ethic, compassion, and self-development. 
	Keep Koding, Keep growing.
	Regards,
	Team Koders 
	Mentoring you to your full potential.
	""".format(name)

	# turn these into plain/html MIMEText objects

	part1 = MIMEText(text,'plain')

	# Add HTML/plain-text part to MIMEMultipart message
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

	# create the plain text and html version of your message

	text = """Hello, Koder {}>,
	We have had a lot of fun developing your vision through our Kodes. Growth and betterment is a never-ending process. <project name> is a timeless project but with time, it would demand changes. Change is inevitable and therefore to keep up with this fast-paced world of reorientation, we would like to suggest some pivotal changes in <project name>. These changes would ensure that our beloved baby kodes are keeping up with the test of time. 
	We are always a call away to address all your queries and to give you an insight into our understandings of <project name>. For your ease, we have also attached the document suggesting the same. 
	Time and Tide, wait for none
	Regards
	Team Koders
	""".format(name)

	# turn these into plain/html MIMEText objects

	part1 = MIMEText(text,'plain')

	# Add HTML/plain-text part to MIMEMultipart message
	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
		server.login(CREDENTIALS.sender_email, CREDENTIALS.password)
		server.sendmail(CREDENTIALS.sender_email,reciever_email, message.as_string())
