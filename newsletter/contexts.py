from .forms import SubscribeForm


def subscriber_form(request):
    """
    Render subscriber form
    """
    subscriber_form = SubscribeForm()

    context = {
        'subscriber_form': subscriber_form,
    }

    return context
