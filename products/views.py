from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category

def all_products(request):
    """
    Returns all products in :model:`products.Product`

    **Context**

    ``products``
        All instances of :model:`products.Product`

    **Template**

    :template:`products/all_products.html`

    """
    products = Product.objects.all()

    query = None
    category = None
    on_sale = None
    sort = None
    direction = None

    if request.GET:
        # Sort results
        if 'sort' in request.GET:
            sort_value = request.GET['sort']
            sort = sort_value
            if sort_value == 'name':
                sort_value = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
                if sort_value == 'category':
                    sort_value = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sort_value = f'-{sort_value}'
            products = products.order_by(sort_value)
        # Filter by category
        if 'category' in request.GET:
            category = request.GET['category'].split(',')
            products = products.filter(category__name__in=category)
            category = Category.objects.filter(name__in=category)
        # Filter products that are on sale
        if 'on_sale' in request.GET:
            products = products.filter(on_sale=True)
            on_sale = True
        # Search function
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter search criteria")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    return render(
        request,
        'products/products.html',
        {'products': products,
         'current_sorting': current_sorting,
         'search_term': query,
         'category': category,
         'on_sale': on_sale,

         }
        )


def product_detail(request, product_id):
    """ 
    Display an individual :model:`products.Product`

    **Context**

    **Template**

    :template:`products/product_detail.html`
    """
    product = get_object_or_404(Product, pk=product_id)

    return render(
        request,
        'products/product_detail.html',
        {"product": product,}
    )