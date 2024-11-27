from django.shortcuts import render, get_object_or_404

from .models import UserProfile


def profile(request):
    """
    Renders profile information about the selected user.

    **Context**

    ``profile``
        An instance of :model:`profiles.Profile`

    **Template**

    :template:`profiles/profile.html`
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    template = 'profiles/profile.html'
    context = {'profile': profile}
    return render(request, template, context)
