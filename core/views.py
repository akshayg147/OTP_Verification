from django.shortcuts import render, redirect
from django.conf import settings
import random
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from .models import Verify

def home(request):
    if request.method == 'POST':
        # The to_be_Sent variable is flag which decides the email should be sent or not
        to_be_Sent = 1
        global user_email
        #taking the email address of the user from the form
        user_email = request.POST['email']
        user = None
        if Verify.objects.filter(email=user_email).exists():
            user = Verify.objects.get(email=user_email)
            if user != None:
                # to check if the user is has already been registered or not
                if user.verified:
                    to_be_Sent == 0 #user already exists and is verified, so no need to send email.
                    return render(request, 'success.html',{"message":"already registered"})
        #lese the mail has to be sent for verification.
        if to_be_Sent == 1 and user == None:
            global new
            z = 'abcdefghij1234567890klmnopqrstuvwxyz'
            global otp
            otp = ''
            #generating random OTP
            for i in range(6):
                otp += ''.join(random.choice(z))
            try:
                #Rendering the HTML template which will be sent as email with OTP.
                msg_html = render_to_string('otp_tem.html', {'otp': otp})
                #sending the Email
                send_mail(
                    'OTP for socialgram',
                    'Thanks for registering with us,Your OTP is'+' \n'+ otp,
                     settings.EMAIL_HOST_USER,
                     [user_email,],
                     html_message=msg_html,
                     fail_silently=False,
                )
            except Exception as e:
                #if exception arise while sending email then error will be shown on the front page.
                return render(request,'verification.html',{'messages': ["Error occured while sending email"]})
            finally:
                return redirect('verification')
    else:
        return render(request,'Email.html')


def verfication(request):
    if request.method == 'POST':
        #Checking whther the otp given by user is correct or not
        ot = request.POST['otp']
        #If the user exists but not verified.
        if Verify.objects.filter(email=user_email).exists():
            if not Verify.objects.get(email=user_email).verified:
                return render(request,'Email.html')
        if ot == otp:
            #if OTP entered by user is correct then user is verified and would be stored into database.
            new = Verify.objects.create(email=user_email)
            new.verified = True
            new.save()
            #send to the final success page
            return render(request,'success.html')
        else:
            #if OTP is incorrect then sending the message of wrong otp.
            return render(request,'verification.html',{'messages': ['Wrong otp']})
    else:
        #To tell the user email has been sent to the given email ID.
        messages.success(request, 'otp sent to {}'.format(user_email))
        return render(request,'verification.html')




