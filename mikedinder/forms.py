from django import forms
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.safestring import mark_safe


class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name"
            }
        )
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last Name"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email Address"
            }
        )
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone Number"
            }
        )
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Your message...",
                "rows": 5
            }
        )
    )

    # # Initialize Form Fields
    # def __init__(self, *args, **kwargs):
    #     super(ContactForm, self).__init__(*args, **kwargs)

    # def is_valid(self):
    #     ret = forms.Form.is_valid(self)

    #     for f in self.errors:
    #         self.fields[f].widget.attrs.update({'class': self.fields[f].widget.attrs.get('class', '') + ' error'})

    #     return ret

    # # Append Invalid Data To Context
    # def update_Context_With_Invalid_Response(self, form, context):
    #     #pageid = context['pageid']

    #     context = {
    #         'form': form
    #     }

    #     return context

    # # Clean Phone Number Field
    # def clean_phone_Number(self):
    #     data = self.cleaned_data['phone_Number']

    #     #print (data)

    #     return data

    # # Send Success Email - Using The self.cleaned_data Dictionary
    # def sendEmail(self, form):
    #     #print (form.cleaned_data)

    #     phone_Number = self.request.POST.get('phone_Number', '')

    #     phone_Number_Cleaned = phone_Number

    #     replace=['(',')']

    #     for i in replace:
    #         phone_Number_Cleaned = phone_Number_Cleaned.replace(i,'')

    #     phone_Number_Cleaned = phone_Number_Cleaned.replace(' ','-')

    #     # Construct Body Of Email
    #     template = get_template('contacts/email/contact_email.html')
    #     context  = {
    #         'site': Site.objects.get_current(),
    #         'full_Name': form.cleaned_data.get('full_Name'),
    #         'email_Field': form.cleaned_data.get('email_Field'),
    #         'phone_Number': phone_Number,
    #         'phone_Number_Cleaned': phone_Number_Cleaned,
    #         'subject': form.cleaned_data.get('subject'),
    #         'message': form.cleaned_data.get('message'),
    #     }

    #     subject = form.cleaned_data.get('subject')

    #     if subject == None:
    #         subject = 'New Contact Form Submission'
    #     else:
    #         subject = 'New Contact Form Submission - ' + form.cleaned_data.get('subject')

    #     # Construct HTML Email With Context Objects
    #     msg_html = template.render(context)

    #     # Format Email Headers
    #     email = EmailMessage(
    #         subject = subject,
    #         body = msg_html,
    #         from_email = 'Connect-IO - Custom Software Solutions',
    #         reply_to = [settings.SERVER_EMAIL],
    #         cc = [],
    #         bcc = [],
    #         # to = [settings.DEFAULT_TEST_EMAIL],
    #         to = [settings.DEFAULT_FROM_EMAIL],
    #         attachments = [],
    #         headers = {}
    #     )

    #     # Change Message From Text/Plain to Text/HTML
    #     email.content_subtype = 'html'

    #     # Fire Off Success Email
    #     email.send()
