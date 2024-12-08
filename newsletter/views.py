from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import Subscriber
from .forms import SubscribeForm


def subscribe(request):
    """
    Allow user to subscribe to the newsletter

    **Context**

    ``subscribe_form``
        An instance of of :form:`newsletter.SubscriberForm`
    """
    # Inspiration taken from:
    # Codemy - https://www.youtube.com/watch?v=xNqnHmXIuzU and 
    # Joshyvibes - https://www.youtube.com/watch?v=LL6qXu8FmVo
    subscribe_form = SubscribeForm(data=request.POST or None)

    if request.method == 'POST':
        if subscribe_form.is_valid():
            subscriber = subscribe_form.save()
            messages.success(
                request, 
                f"{subscriber.email} has been added! \
                    Check your emails for some woolly good news!"
            )
            # send a welcome email to the user
            email_subject = 'Welcome to Woolly family!'
            recipient = subscriber.email
            content = render_to_string(
            'newsletter/confirmation_emails/welcome_email.txt')

            send_mail(
                email_subject,
                content,
                settings.DEFAULT_FROM_EMAIL,
                ['recipient'],
            )
        else:
            messages.error(
                request,
                "An error has occured! Please check that you \
                    spelt your email correctly \
                    and that you have not subscribed already!"
            )

        # Get the url of the previous page the user was on
        previous_url = request.META.get('HTTP_REFERER')

        return (HttpResponseRedirect(previous_url))
