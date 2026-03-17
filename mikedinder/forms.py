from django import forms
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.safestring import mark_safe


class ContactForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }
        )
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }
        )
    )
    email = forms.EmailField(
        label='Email Address',
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }
        )
    )
    phone = forms.CharField(
        label='Phone Number',
        max_length=14,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }
        )
    )
    message = forms.CharField(
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Message...',
                'rows': 15
            }
        )
    )
