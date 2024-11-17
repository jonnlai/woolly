from django.shortcuts import render


def view_bag(request):
    """
    Renders the bag contents page

    **Context**

    **Template**

    :template:`bag/bag.html`
    """
    return render(
        request,
        'bag/bag.html'
        )
