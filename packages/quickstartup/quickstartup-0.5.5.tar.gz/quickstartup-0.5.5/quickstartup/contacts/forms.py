# coding: utf-8


from django import forms
from django.utils.translation import ugettext_lazy as _

from ..core.fields import AntiSpamField
from ..widgets import EmailInput, PhoneInput
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "phone", "message", "antispam")

    name = forms.CharField(label=_("Name"), max_length=255)
    email = forms.EmailField(label=_("E-mail"), max_length=255, widget=EmailInput())
    phone = forms.CharField(label=_("Phone"), max_length=100, widget=PhoneInput(), required=False)
    message = forms.CharField(label=_("Message"), widget=forms.Textarea(attrs={'rows': 5}))
    antispam = AntiSpamField()
