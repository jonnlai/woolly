from django.shortcuts import (
    render,
    redirect,
    reverse,
    HttpResponse,
    get_object_or_404,
)
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """
    Renders the bag contents page

    **Template**

    :template:`bag/bag.html`
    """
    return render(
        request,
        'bag/bag.html'
        )


def add_to_bag(request, item_id):
    """
     Adds a quantity of the specified product to the shopping bag
     """
    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    stock_amount = product.stock_amount

    if item_id in list(bag.keys()):
        # If product in bag check that the total amount requested
        # is equal to or less than amount in stock
        if bag[item_id] + quantity <= stock_amount:
            bag[item_id] += quantity
            messages.success(
                request,
                f'Updated {product.name} quantity to {bag[item_id]}'
            )
        else:
            quantity = quantity
            messages.error(
                request,
                f'Unable to process your request. \
                    Only  {stock_amount} x {product.name} left in stock')
    else:
        if quantity <= stock_amount:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')
        else:
            messages.error(
                request,
                f'Unable to process your request. \
                    Only {stock_amount} x {product.name} left in stock')

    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified product to the specified amount
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})
    stock_amount = product.stock_amount

    if quantity > 0:
        # Check that total amount requested is less than
        # or equal to the amount in stock
        if quantity <= stock_amount:
            bag[item_id] = quantity
            messages.success(
                request,
                f'Updated {product.name} quantity to {bag[item_id]}'
            )
        else:
            quantity = quantity
            messages.error(
                request,
                f'Unable to process your request. \
                    Only  {stock_amount} x {product.name} left in stock')
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag

    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove the item from the shopping bag
    """
    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
