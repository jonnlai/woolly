from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


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


def add_product(request):
    """
    Allow administrator to add a new product

    **Context**

    ``product_form``
        An instance of of :form:`products.ProductForm`

    ** Template **

    :template:`products/add_product.html`
    """
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        product_form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'product_form': product_form,
    }
    return render(request, template, context)

def edit_product(request, product_id):
    """
    Display :form:`products.ProductForm` for edit.

    ** Context **

    ``product``
        An instance of :model:`products.Product`
    ``product_form``
        An instance of :form:`products.ProductForm`

    **Template**

    :template:`products/edit_product.html`
    """
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:    
        product_form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'product_form': product_form,
        'product': product,
    }

    return render(request, template, context)