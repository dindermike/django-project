from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from mikedinder.forms import ContactForm


class ContactFormView(FormView):
    template_name = 'mikedinder/pages/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('mikedinder:contact_success')

    def form_valid(self, form):
        data = form.cleaned_data

        subject = f'New Contact Form Submission from {data["first_name"]} {data["last_name"]}'
        from_email = settings.DEFAULT_FROM_EMAIL
        reply_to = [data['email']]
        send_to = [settings.CONTACT_RECIPIENT_EMAIL]

        # Render the HTML Email Body
        html_body = render_to_string(
            'mikedinder/emails/contact_email.html',
            {'data': data}
        )

        # Plain-text fallback
        plain_body = (
            f'Name: {data["first_name"]} {data["last_name"]}\n'
            f'Email: {data["email"]}\n'
            f'Phone: {data.get("phone", "N/A")}\n\n'
            f'Message:\n{data["body"]}'
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_body,
            from_email=from_email,
            to=send_to,
            reply_to=reply_to,
        )
        email.attach_alternative(html_body, 'text/html')
        email.send(fail_silently=False)

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
