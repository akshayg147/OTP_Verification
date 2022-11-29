from django.shortcuts import render, redirect
from django.conf import settings
import random
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from .models import Verify

def home(request):
    if request.method == 'POST':
        to_be_Sent = 1
        global user_email
        user_email = request.POST['email']
        user = None
        if Verify.objects.filter(email=user_email).exists():
            user = Verify.objects.get(email=user_email)
            print(user)
            if user != None:
                print("inside",user.email,user.verified,user.otp)
                if user.verified:
                    print('I was here')
                    to_be_Sent == 0
                    return render(request, 'success.html',{"message":"already registered"})
        if to_be_Sent == 1 and user == None:
            global new
            # new = Verify.objects.create(email=user_email)
            z = 'abcdefghij1234567890klmnopqrstuvwxyz'
            global otp
            otp = ''
            for i in range(6):
                otp += ''.join(random.choice(z))
            try:
                print(otp)
                msg_html = render_to_string('otp_tem.html', {'otp': otp})
                send_mail(
                    'OTP for socialgram',
                    'Thanks for registering with us,Your OTP is'+' \n'+ otp,
                     settings.EMAIL_HOST_USER,
                     [user_email,],
                     html_message=msg_html,
                     fail_silently=False,
                )
                # new.otp = otp
            except Exception as e:
                print(e)
                return render(request,'verification.html',{'messages': ["Error occured while sending email"]})
            finally:
                return redirect('verification')
    else:
        return render(request,'Email.html')
def verfication(request):
    if request.method == 'POST':
        print('hey there')
        ot = request.POST['otp']
        if Verify.objects.filter(email=user_email).exists() and new.verified:
            return render(request,'success.html')
        if ot == otp:
            new = Verify.objects.create(email=user_email)
            new.verified = True
            new.save()
            return render(request,'success.html')
        else:
            return render(request,'verification.html',{'messages': ['Wrong otp']})
    else:
        print('success')
        messages.success(request, 'otp sent to {}'.format(user_email))
        return render(request,'verification.html')




