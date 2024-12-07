from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.exceptions import ObjectDoesNotExist

from .models import Product, Category
from .forms import ProductForm

from profiles.models import UserProfile
from wishlist.models import Wishlist
from reviews.models import Review
from reviews.forms import ReviewForm
from checkout.models import Order


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

        ``product``
            An instance of :model:`products.Product`
        ``profile``
            An instance of :model:`profiles.UserProfile`
        ``wishlist``
            An instance of :model:`wishlist.Wishlist`
        ``reviews``
            A list of reviews relating to ``product``
        ``review_form``
            A instance of :form:`reviews.ReviewForm`

    **Template**

    :template:`products/product_detail.html`
    """
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)
    review_authors = list(reviews.values_list(
        "review_author__username", flat="True"))

    if request.user.is_authenticated:
        # Get profile, wishlist and order if user is authenticated
        profile = get_object_or_404(UserProfile, user=request.user)
        wishlist = list(Wishlist.objects.filter(
            user_profile=profile).values_list(
                "wished_product__name", flat="True"))
        orders = list(Order.objects.filter(
            user_profile=profile).values_list(
                "lineitems__product__name", flat="True"))
    else:
        # If user is not authenticated, set values to False
        wishlist = False
        profile = False
        orders = False

    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.review_author = request.user
            review.product = product
            review.save()
            messages.success(request, 'Your review has been added')
            return redirect('product_detail', product_id)
        else:
            messages.error(request, 'Unable to save your review. \
                Please try again.')

    review_form = ReviewForm()

    return render(
        request,
        'products/product_detail.html',
        {"product": product,
         "wishlist": wishlist,
         "reviews": reviews,
         "review_form": review_form,
         "review_authors": review_authors,
         "orders": orders}
    )

@login_required
def add_product(request):
    """
    Allow administrator to add a new product

    **Context**

    ``product_form``
        An instance of of :form:`products.ProductForm`

    ** Template **

    :template:`products/add_product.html`
    """
    if not request.user.is_superuser:
        messages.error(request,
            'Sorry, only store owners can access this page')
        return redirect(reverse('home'))
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. \
                Please ensure the form is valid.')
    else:
        product_form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'product_form': product_form,
    }
    return render(request, template, context)


@login_required
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
    if not request.user.is_superuser:
        messages.error(request,
            'Sorry, only store owners can access this page')
        return redirect(reverse('home'))

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


@login_required
def delete_product(request, product_id):
    """
    Delete a product

    **Context**

    ``product``
        An instance of :model:`products.Product`
    """
    if not request.user.is_superuser:
        messages.error(request,
            'Sorry, only store owners can access this page')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    
    return redirect(reverse('products'))


def delete_review(request, product_id, review_id):
    """
    Delete a review
    """
    review = get_object_or_404(Review, pk=review_id)
    product = get_object_or_404(Product, pk=product_id)

    if review.review_author == request.user:
        review.delete()
        messages.success(request, 'Your review has been deleted!')
    else:
        messages.error(request, 'You can only delete your own reviews!')

    return redirect('product_detail', product_id)
