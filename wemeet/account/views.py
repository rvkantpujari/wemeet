from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views import View
from .forms import * 
from django.contrib.auth.models import User
from django.contrib import auth
from datetime import datetime
from django.contrib.auth import authenticate, login, logout,\
    update_session_auth_hash
from random import randint
from .models import UserDetails
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
import os
from django.conf import settings
from PIL import Image
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.utils.html import strip_tags


class LoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            fm = LoginForm()
            return render(request, 'account/login.html', {'form':fm})
        else:
            return redirect('home')

    def post(self, request):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        fm = LoginForm()
        if not user:
            return render(request, 'account/login.html', {'form': fm,
                'message':'Email Does not Exist'})

        uname = user.username
        user = auth.authenticate(username=uname, password=password)
        
        if user is None:
            fm = LoginForm()
            return render(request, 'account/login.html', {'form': fm,
                'message':'Email and Password didnot match'})

        verified = UserDetails.objects.get(email=user).isVerified
        
        if not verified:
            return render(request, 'account/login.html', {'form': fm,
                'message':'Please verify your E-mail. link sent to your email.'})

        auth.login(request, user)
        user.lastLogin = datetime.now()
        user.save()
        return redirect('home')
    

class Register(View):
    def get(self, request):
        if not request.user.is_authenticated:
            fm = SignUpForm()

            return render(request, 'account/register.html', {'form':fm})
        else:
            return HttpResponseRedirect('/account/profile/')

    def post(self, request):

        fname = request.POST['firstName']
        lname = request.POST['lastName']
        email = request.POST['email']

        user = User.objects.filter(email = email)

        if user:
            print("email exist: ", user)
            fm = SignUpForm()
            return render(request, 'account/register.html', {'form':fm,
                'message':'E-mail already exist'})

        uname = self.generate_username(fname, lname)

        user = User(
            email = email,
            first_name = fname, last_name = lname,
            username = uname
            )

        user.set_password(request.POST['password'])
        user.save()

        profilePic = '/media/profilePics/default.png'
        userDetails = UserDetails(email=user, profilePic=profilePic)
        userDetails.save()

        current_site = get_current_site(request)
        EmailTitle = 'Activate your WeMeet Account.'
        html_message = render_to_string('emails/EmailActivation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
        plain_message = strip_tags(html_message)
        Emailreceiver = user.email
        send_mail(
                EmailTitle,
                plain_message,
                'wemeetcare@gmail.com',
                [Emailreceiver],
                fail_silently = False,
                html_message=html_message
            )
        return redirect('/account/login/')

    def generate_username(self, fname, lname):
        uname = fname.lower() + lname.lower()
        while(1):
            uname += str(randint(1000, 9999))
            u = User.objects.filter(username = uname)
            if not u:
                return uname


def activateAccount(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        userDetails = UserDetails.objects.get(email=user)
        userDetails.isVerified = True
        userDetails.save()
        # login(request, user)
        # return redirect('home' )
        return render(request, 'emails/EmailActivationSuccess.html')
    else:
        return HttpResponse('Activation link is invalid!')


@method_decorator(login_required, name='dispatch')
class Profile(View):
    def get(self, request):
        user = UserDetails.objects.filter(email__id = request.user.id)[0]
        fm = profileForm()
        return render(request, 'account/profile.html', {'user':user,'form': fm})


    def post(self, request):
        curr_user = request.user
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        dob = request.POST['dob']
        gender = None
        mobile = request.POST['mobile']
        alternateEmail = request.POST['alternateEmail']

        if not mobile:
            mobile = None
        if not alternateEmail:
            alternateEmail = None
        if request.POST.get('gender'):
            gender = request.POST['gender']
        if not dob:
            dob = None

        User.objects.filter(pk=curr_user.id).update(
                first_name = first_name,
                last_name = last_name
            )
        UserDetails.objects.filter(pk = curr_user.id).update(
                dob = dob,
                gender = gender,
                mobile = mobile,
                alternateEmail = alternateEmail
            )
        request_file = request.FILES['profilePic'] if 'profilePic' in request.FILES else None
        
        if request_file:

            profilePicName = curr_user.username+'.png'
            profilePicPath = 'media/profilePics/' + profilePicName

            storeAt = os.path.join(settings.STATIC_DIR, 'media/profilePics/')

            fs = FileSystemStorage(storeAt)

            if os.path.exists(settings.STATIC_DIR+ '/' + profilePicPath):
                os.remove(os.path.join(settings.STATIC_DIR, profilePicPath))

            file = fs.save(profilePicName, request_file)            

            image = Image.open(storeAt + profilePicName)
            
            image = image.resize((820, 800), Image.ANTIALIAS)
            image.save(storeAt + profilePicName, format='PNG')

            UserDetails.objects.filter(pk = curr_user.id).update(
                profilePic = profilePicPath
            )

        return redirect('profile')


@method_decorator(login_required, name='dispatch')
class ChangeUserPassowrd(View):
    def get(self, request):
        if not request.user.is_authenticated:
            HttpResponseRedirect('/account/profile/')
        fm = PasswordChangeForm(user = request.user)
        return render(request, 'account/changepassword.html', {'form':fm})

    def post(self, request):
        fm = PasswordChangeForm(user = request.user, data = request.POST)

        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            # return HttpResponseRedirect('/account/profile/')
            return redirect('home')
        return render(request, 'account/changepassword.html', {'form':fm})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect('/account/login/')


