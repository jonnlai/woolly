from django.shortcuts import render

def index(request):
    """
    Returns the home page.

    **Context**


    **Template**

    :template:`home/index.html`
    """
    return render(request, 'home/index.html')
