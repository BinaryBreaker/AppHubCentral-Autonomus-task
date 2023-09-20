from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class HTMLMessageMixin:
    def send_html_email(self, subject, template_name, context, recipient_list):
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        email = EmailMultiAlternatives(subject, html_message, to=recipient_list)
        email.attach_alternative(html_message, "text/html")
        email.send()
