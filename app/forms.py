from django import forms
from .models import Customer,Blog
from .validation import *

class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Please enter a strong password'}),help_text='Ensure this field must have a lowercase alphabet, an uppercase alphabet, one digit and a special character from [!@#$%]',validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm your password'}),help_text='Please enter your password again')
    
    class Meta:
        model = Customer
        fields = ('full_name','email','mobile','password')

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return confirm_password


class BlogForm(forms.Form):
    
    title = forms.CharField(min_length=2,help_text='Enter the title of the blog',strip=True,required=True,widget=forms.TextInput(attrs={'placeholder':'Enter the title of the blog','class':'w-100 form-control'}))
    blog = forms.CharField(min_length=2,help_text='Enter the full description of the blog',strip=True,required=True,widget=forms.Textarea(attrs={'placeholder':'Enter the full description of the blog','class':'w-100 form-control'}))
    category = forms.CharField(strip=True,required=True,help_text='Enter the category of the blog',widget=forms.TextInput(attrs={'placeholder':'Enter the category of the blog','class':'w-100 form-control'}))

    