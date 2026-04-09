#from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account

class SignUpForm(forms.ModelForm):
     first_name = forms.CharField(label="",max_length=30, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
     last_name = forms.CharField(label="",max_length=60,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
     password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password','class': 'form-control',}),help_text='<ul class="form-text text-muted small"><li>Your password can\'t be too similar your infamation personal</li><li>Your password must contain at least 8 caracter.</li><li>Your password can\'t be a commoly used password</li><li>Your password can\'t be entirely numeric.</li></ul>')
     confirm_password= forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control',  }),help_text='<span class="form-text text-muted"><small>Enter the same as before, for verification</small></span>')

     class Meta:
          model = Account
          fields = ('username','first_name', 'last_name', 'password', 'confirm_password')

     def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text ='<span class="form-text text-muted"><small>Required. 150 character or fewer, digits and @/./ +/-/_only</small></span>'

    