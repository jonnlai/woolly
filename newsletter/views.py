from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Subscriber
from .forms import SubscribeForm


def subscribe(request):
    """
    Allow user to subscribe to the newsletter

    **Context**

    ``subscribe_form``
        An instance of of :form:`newsletter.SubscriberForm`
    """

    subscribe_form = SubscribeForm(data=request.POST or None)

    if request.method == 'POST':
        if subscribe_form.is_valid():
            subscriber = subscribe_form.save()
            messages.success(
                request, 
                f"{subscriber.email} has been added! \
                    Check your emails for some woolly good news!"
            )
        else:
            messages.error(
                request,
                f"Error adding {subscriber.email}. Please check that you \
                    spelt the address correctly \
                    and that you have subscribed already!"
            )

        # Get the url of the previous page the user was on
        previous_url = request.META.get('HTTP_REFERER')

        return (HttpResponseRedirect(previous_url))
