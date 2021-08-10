from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import modelform_factory

import voters.views
from voters.models import Voter
import random
import http.client
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.cache import cache
import vote
# Create your views here.

LoginForm = modelform_factory(Voter, fields=("name", "user", "mobile"))


def login(request):
    if request.method == "POST":
        name = request.POST.get('name')
        user = request.POST.get('user')
        mobile = request.POST.get('mobile')
        #print(name, user, mobile)
        voter=Voter.objects.filter(user = user).first()
        if voter == None:
            form = LoginForm
            return render(request, "login_page/login.html",
                          {"form": form, "message": "User_Name Not Found!"})
        #print(voter.mobile)
        if voter.name != name:
            form=LoginForm
            return render(request,"login_page/login.html",
                          {"form": form, "message" : "Wrong Name!"})
        if voter.mobile == mobile:
            otp = str(random.randint(1000, 9999))
            Voter.objects.filter(user=user).update(otp=otp)
            send_otp(mobile,otp)
            request.session['mobile'] = mobile
            request.session['user'] = user

            return redirect('otp')
        else:
            #return HttpResponse("Wrong")
            form=LoginForm
            return render(request, "login_page/login.html",
                          {"form": form, "message" : "Wrong Mobile!"})

    else:
        form=LoginForm()
        return render(request, "login_page/login.html",
                  {"form": form, "message" : "Enter details"})



def otp(request):


    mobile = request.session['mobile']
    user = request.session['user']
    voter = Voter.objects.filter(user=user).first()
    name= voter.name
    context = {'mobile': mobile, 'user' : user, 'name' : name}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        voter = Voter.objects.filter(mobile=mobile).first()

        if otp == voter.otp:
            cache.set('curr_voter',mobile)
            settings.BOOL_KEY = True
            return redirect('http://127.0.0.1:8000/vote/')
            #return render(request,'vote/election.html', context)
            #return redirect(voters.views.detail(request, user))
        else:
            #print('Wrong')

            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'login_page/otp.html', context)

    return render(request, 'login_page/otp.html', context)

def send_otp(mobile , otp):
    #print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    headers = { 'content-type': "application/json" }
    #url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    url = "http://control.msg91.com/api/sendotp.php?otp=" + otp + "&message=" + "Yourotpis" + otp + "&mobile=" + mobile + "&authkey=" + authkey + "&country=91"
    #url = "https://api.msg91.com/api/v5/otp?template_id=60b5c98f1746775f101f3a39&mobile=" + mobile + "&authkey=361663A7d44XXUTD60b5c0f8P1"
    conn.request("GET", url , headers=headers)
    res = conn.getresponse()
    data = res.read()
    #print(data)
    return None