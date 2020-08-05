from django import forms
from django.core import validators


class regForm(forms.Form):
    firstName = forms.CharField(min_length=3, max_length=20, widget=forms.TextInput(attrs={'class':'form-control form-input', 'placeholder': 'John'}))
    lastName = forms.CharField(min_length=3, max_length=20, label='Last Name: ', widget=forms.TextInput(attrs={'class':'form-control form-input', 'placeholder': 'Doe'}))
    email = forms.EmailField(validators=[validators.MaxLengthValidator(50)], label='Email: ', widget=forms.TextInput(attrs={'class':'form-control form-input', 'placeholder': 'johndoe@gmail.com'}))
    password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control form-input'}))
    repassword = forms.CharField(min_length=8, max_length=32, label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control form-input'}))
    
    def clean(self):
        cleaned_data = super(regForm, self).clean()
        valPass = cleaned_data.get('password')
        valRePass = cleaned_data.get('repassword')
        if valPass != valRePass:
            self.add_error('password','Passwords did not match.')


class loginForm(forms.Form):
    email = forms.EmailField(max_length=50, label='Email: ', widget=forms.TextInput(attrs={'class':'form-control form-input', 'placeholder': 'johndoe@gmail.com'}))
    password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control form-input'}))


class DateInput(forms.DateInput):
    input_type = 'date'


class profileForm(forms.Form):
    email = forms.EmailField(validators=[validators.MaxLengthValidator(50)], label='Email: ', widget=forms.TextInput(attrs={'class': 'form-control form-input col-md-3', 'placeholder': 'johndoe@gmail.com'}))

    alternateEmail = forms.EmailField(required=False, validators=[validators.MaxLengthValidator(50)], label='Alternate Email: ', widget=forms.TextInput(attrs={'class': 'form-control form-input', 'placeholder': 'johndoe@gmail.com'}))

    mobile = forms.IntegerField(required=False, validators=[validators.MaxLengthValidator(10), validators.MinLengthValidator(10)],min_value=6000000000, max_value=9999999999,widget=forms.TextInput(attrs={'class': 'form-control form-input', 'placeholder': '9012345678'}))

    firstName = forms.CharField(label='First Name: ',min_length=3, max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-input', 'placeholder': 'John'}))

    #middleName = forms.CharField(min_length=3, max_length=20, label='Middle Name: ', required=False, widget=forms.TextInput(attrs={'class':'form-control form-input', 'placeholder': 'Ivy'}))

    lastName = forms.CharField(min_length=3, max_length=20, label='Last Name: ', widget=forms.TextInput(attrs={'class': 'form-control form-input col-md-3', 'placeholder': 'Doe'}))
    
    dob = forms.DateField(required=False,label='Date of Birth: ', widget=DateInput(attrs={'class': 'form-control form-input'}))

    CHOICES = [(0,'Male'),(1,'Female'),(2,'Other')]
    gender= forms.IntegerField(required=False, label='Gender: ', widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'custom-control custom-radio custom-control-inline'}))

    profilePic = forms.ImageField(required=False, label='Upload Profile Picture')


class resetPasswordForm(forms.Form):
    oldPassword = forms.CharField(label='Old Password: ',min_length=8, max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control form-input'}))
    newPassword = forms.CharField(label='New Password: ', min_length=8, max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control form-input'}))
    newRePassword = forms.CharField(label='Confirm Password: ', min_length=8, max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control form-input'}))
    
    def clean(self):
        cleaned_data = super(resetPasswordForm, self).clean()
        valPass = cleaned_data.get('newPassword')
        valRePass = cleaned_data.get('newRePassword')
        if valPass != valRePass:
            self.add_error('newPassword','Passwords did not match.')

class forgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=50, label='Email: ', widget=forms.TextInput(attrs={'class':'form-control form-input', 'placeholder': 'johndoe@gmail.com'}))