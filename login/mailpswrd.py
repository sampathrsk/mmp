
import pswrd
import smtplib
import views

def mailpswrd(email):
	server = smtplib.SMTP('smtp.gmail.com',587)

	server.starttls()
	server.login("captainbatman16@gmail.com","12345678cap")
	c = pswrd.pswrd()
	name = ''
	d = views.recover.send(name)
	msg = "hello check. " + "this is a trial" + "\n\n\n" + "YOUR NEW PASSWORD IS: " + c + "\n\n\n" + "please keep your password safe " + "        "  + d

##msg = c
	server.sendmail("captainbatman16@gmail.com",email, msg)
	return(c)

