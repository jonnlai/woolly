from django.shortcuts import render, reverse, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Review
from .forms import ReviewForm
from products.models import Product


def edit_review(request, product_id, review_id):
    """
    Edit a selected instance of :model:`reviews.Review`

    **Context**

    ``review``
        An instance of :model:`reviews.Review`
    ``product``
        An instance of :model:`products.Product`
    ``review_form``
        An instance of :form:`reviews.ReviewForm`

    **Template**

    :template:`reviews/edit_review.html`

    """
    review = get_object_or_404(Review, pk=review_id)
    product = get_object_or_404(Product, pk=product_id)
    review_form = ReviewForm(instance=review)

    if request.method == "POST":
        review_form = ReviewForm(data=request.POST or None, instance=review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, 'Review updated!')
            return redirect("product_detail", product_id)
        else:
            messages.error(request, 'Error updating review!')


    return render(request,
            "reviews/edit_review.html",
            {"review": review,
            "product": product,
            "review_form": review_form})
