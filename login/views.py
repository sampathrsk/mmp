from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from . import forms
import pswrd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
	##email = request.POST['email']
        password = request.POST['password']
        next_link = request.POST.get('next', False)
        user = authenticate(request, username=username, password=password)
	##user = authenticate(request, email=email, password=password)
        if user is not None:
	    if user.is_active:
            	request.session.set_expiry(3600)
		login(request,user)
            	if next_link:
                	return redirect(next_link)
            	else:
                	return redirect('/form1/')
        else:
            return render(request, 'login/login.html', {'login_form': forms.SignInForm(), 'errors': True})
    else:
        if request.user.is_authenticated:
            return redirect('/form1/')
        else:
            return render(request, 'login/login.html', {'login_form': forms.SignInForm()})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        #return render(request, 'login/login.html', {'logout_message': "You logged out successfully!"})
        return redirect('/accounts/login/')
    else:
        return redirect('/accounts/login/')
        #return render(request, 'login/login.html', {'logout_message': "You are already logged out!"})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        next_link = request.POST.get('next', False)
        extra_fields = {}
        extra_fields['first_name'] = first_name
        extra_fields['last_name'] = last_name
        user = User.objects.create_user(username,email,password,**extra_fields)
        user = authenticate(request,username=username,password=password)
        login(request,user)
        if next_link:
            return redirect(next_link)
        else:
            return redirect('/accounts/login/')
    else:
        return render(request, 'login/register.html', {'registration_form': forms.SignUpForm()})
@login_required()
def changepassword(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        if user.check_password(old_password):
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request,user)
                return redirect('/form1/')
            else:
                return render(request, 'changepassword.html', {'change_password_form': forms.ChangePasswordForm(request.user), 'errors': True, 'error_message': 'Entered New Passwords do not match'})
        else:
            return render(request, 'changepassword.html', {'change_password_form': forms.ChangePasswordForm(request.user), 'errors': True, 'error_message': 'Your Old Password does not match with the User'})
    else:  
        return render(request, 'changepassword.html', {'change_password_form': forms.ChangePasswordForm(request.user)})
def forgot(request):
	return render(request, 'login/forgot.html')

def recover(request):
	email = request.POST['email']
	print("the email is :")
	print(email)
	details = User.objects.get(email=email)
	name = details.username
	print(name)
	today = date.today()
	c = pswrd.pswrd()

	##server = smtplib.SMTP('smtp.gmail.com',587)
       	##server.starttls()
        ##server.login("captainbatman16@gmail.com","12345678cap")
##        msg = BeautifulSoup('login/done.html')

	##msg = "hi"
	subject, from_email, to = 'Subject', 'captainbatman16@gmail.com', email

	html_content = render_to_string('login/email_content.html', {'c':c, 'name':name, 'today':today})
	text_content = strip_tags(html_content)

	msg = EmailMultiAlternatives(subject, text_content, from_email, [to] )
	msg.attach_alternative(html_content, "text/html")
       
       	
	##server.sendmail("captainbatman16@gmail.com", email, msg)
	msg.send()
	print(details.password)
	details.set_password(c)
	details.save()
	return render(request, 'login/done.html')
