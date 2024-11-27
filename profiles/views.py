from django.shortcuts import render


def profile(request):
    """
    Renders profile information about the selected user.

    **Context**

    ``profile``
        An instance of :model:`profiles.Profile`

    **Template**

    :template:`profiles/profile.html`
    """
    template = 'profiles/profile.html'
    context = {}
    return render(request, template, context)
