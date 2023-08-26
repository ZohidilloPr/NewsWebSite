from django import forms
from django.core.mail import send_mail
from captcha.fields import ReCaptchaField
from .models import (Comments, Contact, News)

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = "__all__"


class ContactForm(forms.ModelForm):
    class Meta: 
        model = Contact
        fields = "__all__"

        widgets = {
            "f_name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
            }),
            "subject": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
            }),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"

        def __init__(self, *args, **kwargs):
            super(NewsForm, self).__init__(*args, **kwargs)
            


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField()