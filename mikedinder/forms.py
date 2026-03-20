from django import forms
from django.core.validators import RegexValidator


class ContactForm(forms.Form):
    """
    Contact Mike Dinder Form
    """
    error_css_class = 'is-invalid'
    required_css_class = 'is-required'

    # Regex breakdown:
    # \( and \): literal parentheses
    # \d{3}: exactly 3 digits
    # \s: a single space
    # -: a literal dash
    phone_regex = RegexValidator(
        regex=r'^\(\d{3}\)\s\d{3}-\d{4}$',
        message="Phone number must be entered in the format: '(555) 555-5555'."
    )

    # Regex breakdown:
    # ^[ -~]*$ matches everything from ' ' (space) to '~' (tilde) in ASCII.
    # This covers: a-z, A-Z, 0-9, and all standard special characters:
    # ! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~
    english_and_symbols = RegexValidator(
        regex=r'^[ -~]*$',
        message="Please use only English language and standard punctuation symbols."
    )

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
        validators=[phone_regex],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }
        )
    )
    message = forms.CharField(
        max_length=5000,
        validators=[english_and_symbols],
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Message...',
                'rows': 15
            }
        )
    )
