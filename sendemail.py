from surveillance import out
from graphplot import p

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

sender = 'Sender Email Address'
receivers = ['reciever1' , 'reciever2']

msg = MIMEMultipart()

COMMASPACE = ', '

msg['From'] = sender
msg['To'] = COMMASPACE.join(receivers)

msg['Subject'] = "Alert! Intrution Detected"
body = "Someone just entered your premises. Take Quick Actions!"

msg.attach(MIMEText(body, 'plain'))

# Attaching Video
filename = "video.mp4"
attachment1 = open("video.mp4", "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment1).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment1; filename= %s" % filename)

msg.attach(part)

# Attaching graph
filename = "Graph.html"
attachment2 = open("Graph.html", "rb")
part1 = MIMEBase('application', 'octet-stream')
part1.set_payload((attachment2).read())
encoders.encode_base64(part1)
part1.add_header('Content-Disposition', "attachment2; filename= %s" % filename)

msg.attach(part1)

# Configuring Server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, "password_here")
text = msg.as_string()
server.sendmail(sender, receivers, text)
server.quit()