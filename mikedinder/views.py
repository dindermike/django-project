from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from mikedinder.forms import ContactForm


def preview_contact_email(request):
    """
    Preview View of the Email Sent to the Site Owner when a Contact Form is Submitted, for Development Use Only.
    """
    # Define the Form Rendered Context
    context = {
        'data': {
            'first_name': 'Mike',
            'last_name': 'Dinder',
            'email': 'dindermike@hotmail.com',
            'phone': '(623) 552-9371',
            'message': 'Testing 1.2.3...',
        }
    }

    # In this view, we return the rendered HTML string as a standard HTTP response for previewing
    return render(request, 'mikedinder/emails/contact_email.html', context)


def preview_contact_user_email(request):
    """
    Preview View of the Email Sent to the User who Submitted the Form, for Development Use Only.
    """
    # Define the Form Rendered Context
    context = {
        'data': {
            'first_name': 'Mike',
            'last_name': 'Dinder',
            'email': 'dindermike@hotmail.com',
            'phone': '(623) 552-9371',
            'message': 'Testing 1.2.3...',
        }
    }

    # In this view, we return the rendered HTML string as a standard HTTP response for previewing
    return render(request, 'mikedinder/emails/contact_user_email.html', context)


class ContactFormView(FormView):
    template_name = 'mikedinder/pages/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('mikedinder:contact_success')

    def form_valid(self, form):
        data = form.cleaned_data

        subject = f'New Contact Form Submission from {data["first_name"]} {data["last_name"]}'
        user_subject = settings.EMAIL_SUBJECT_PREFIX + 'Thank You For Contacting Me'
        from_email = settings.DEFAULT_FROM_EMAIL
        reply_to = [data['email']]
        user_reply_to = [settings.DEFAULT_FROM_EMAIL]
        send_to = [settings.CONTACT_RECIPIENT_EMAIL]
        user_send_to = [data['email']]

        # Render the HTML Email Body
        html_body = render_to_string(
            'mikedinder/emails/contact_email.html',
            {
                'data': data
            },
            request=self.request
        )
        user_html_body = render_to_string(
            'mikedinder/emails/contact_user_email.html',
            {
                'data': data
            },
            request=self.request
        )

        # Plain-Text Fallback
        plain_body = (
            f'Name: {data["first_name"]} {data["last_name"]}\n'
            f'Email: {data["email"]}\n'
            f'Phone: {data["phone"]}\n'
            f'Message: {data["message"]}\n'
        )
        user_plain_body = (
            'Thank you very much for contacting me. I will review your form submission within the next 24-48 hours and '
            'respond accordingly, this does not include weekends or holidays. I look forward to hearing what you have '
            'to say and/or working with you at your company or on your next project.\n\nBelow you can view the '
            'information you sent to me.\n\n\n'
            f'Name: {data["first_name"]} {data["last_name"]}\n'
            f'Email: {data["email"]}\n'
            f'Phone: {data["phone"]}\n'
            f'Message: {data["message"]}\n'
        )

        contact_email = EmailMultiAlternatives(
            subject=subject,
            body=plain_body,
            from_email=from_email,
            to=send_to,
            reply_to=reply_to,
        )
        contact_email.attach_alternative(html_body, 'text/html')
        contact_email.send(fail_silently=False)

        user_email = EmailMultiAlternatives(
            subject=user_subject,
            body=user_plain_body,
            from_email=from_email,
            to=user_send_to,
            reply_to=user_reply_to,
        )
        user_email.attach_alternative(user_html_body, 'text/html')
        user_email.send(fail_silently=False)

        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'mikedinder/pages/contact_success.html'


class LandingView(TemplateView):
    """
    Home/Landing Page
    """
    template_name = 'mikedinder/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['branded_title'] = 'Django'
        context['meta_description'] = 'Django Framework — A comprehensive guide to the history, ecosystem, and usage ' \
            'of the Django web framework.'
        context['page_class'] = 'home-page'
        context['page_id'] = 'home-page'
        context['title'] = 'Django: The Framework for Perfectionists with Deadlines'

        return context
