from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import Group
from .models import Account

class SignUpForm(UserCreationForm):
     
     username = forms.CharField(label="",max_length=30, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}),help_text ='<span class="form-text text-muted"><small>Required. 150 character or fewer, digits and @/./ +/-/_only</small></span>')
     first_name = forms.CharField(label="",max_length=30, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
     last_name = forms.CharField(label="",max_length=60,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
     password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password','class': 'form-control',}),help_text='<ul class="form-text text-muted small"><li>Your password can\'t be too similar your infamation personal</li><li>Your password must contain at least 8 caracter.</li><li>Your password can\'t be a commoly used password</li><li>Your password can\'t be entirely numeric.</li></ul>')
     password2= forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control',  }),help_text='<span class="form-text text-muted"><small>Enter the same as before, for verification</small></span>')
     group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
    )
     class Meta:
          model = User
          fields = ['username','first_name', 'last_name', 'password1', 'password2']

     def __init__(self, *args, **kwargs):
          super(SignUpForm, self).__init__(*args, **kwargs)
          self.fields['group'].widget.attrs['class'] = 'form-control'
          self.fields['group'].widget.attrs['placeholder'] = 'Cardo/Regras'
          self.fields['group'].label = ''

     def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        if commit:
            user.save()
            # Atribui o grupo (role)
            group = self.cleaned_data.get('group')
            if group:
                user.groups.add(group)
        return user
    