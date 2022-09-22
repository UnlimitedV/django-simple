from django.core.mail import EmailMessage, send_mail, mail_admins, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    try:
        # send_mail('subject', 'message', 'A@b.com', ['b@a.ir'])
        # mail_admins('subject', 'message', html_message='message')
        # message = EmailMessage('subject', 'message', 'from@domain.com', ['to@domain.com'])
        # message.attach_file('playground/static/images/dog.jpg')
        # message.send()
        message = BaseEmailMessage(template_name='emails/hello.html', context={'name': 'vahid'})
        message.send(['receiver@domain.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'vahid'})
