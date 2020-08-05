from django.shortcuts import render
from .forms import * 

#regForm, loginForm, profileForm, resetPasswordForm, forgotPasswordForm
# Create your views here.

def login(request):
    if request.method == 'POST':
        fm = loginForm(request.POST)
        if fm.is_valid():
            print('Form validated')
            print('email ', fm.cleaned_data['email'])
    else:
        fm = loginForm()
    return render(request, 'account/login.html', {'form': fm})

def register(request):
    # fm = regForm(auto_id=True, label_suffix=':', initial={'email':'abc@xyz.com'})
    if request.method == 'POST':
        fm = regForm(request.POST)
        if fm.is_valid():
            print('Form validated')
            print('email ', fm.cleaned_data['email'])
    else:
        fm = regForm()
    return render(request, 'account/register.html', {'form': fm})

def profile(request):
    if request.method == 'POST':
        fm = profileForm(request.POST)
        if fm.is_valid():
            print('Form validated')
            print('email ', fm.cleaned_data['email'])
    else:
        fm = profileForm()
    return render(request, 'account/profile.html', {'form': fm})

def resetPassword(request):
    if request.method == 'POST':
        fm = resetPasswordForm(request.POST)
        if fm.is_valid():
            print('Form validated')
            print('email ', fm.cleaned_data['email'])
    else:
        fm = resetPasswordForm()
    return render(request, 'account/reset-password.html', {'form': fm})

def forgotPassword(request):
    if request.method == 'POST':
        fm = forgotPasswordForm(request.POST)
        if fm.is_valid():
            print('Form validated')
            print('email ', fm.cleaned_data['email'])
    else:
        fm = forgotPasswordForm()
    return render(request, 'account/forgot-password.html', {'form': fm})
