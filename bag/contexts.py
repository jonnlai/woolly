from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    discount_amount = 0

    bag = request.session.get('bag', {})

    # Get the discount amount and coupon_code of current session.
    # Comes from coupons.views.py
    # Inspiration taken from https://medium.com/@ayoubennaoui20/
    # integrating-a-coupon-system-into-our-e-commerce-website-700a9e699f2a
    discount_amount = request.session.get('discount_amount')
    coupon_code = request.session.get('coupon_code')

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += item_data * product.product_price
        product_count += item_data
        bag_items.append({
            'item_id': item_id,
            'quantity': item_data,
            'product': product,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    if discount_amount and total > discount_amount + 10:
        grand_total -= discount_amount

    # Delete discount_amount and coupon_code
    # if total is less than discount_amount + 10
    if 'discount_amount' in request.session and total < discount_amount + 10:
        del request.session['discount_amount']
        del request.session['coupon_code']

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'discount_amount': discount_amount,
        'coupon_code': coupon_code,
    }

    return context
