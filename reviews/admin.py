from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'review_author',
        'review_title',
        'review_content',
        'product_rating',
        'created_on',
    )

admin.site.register(Review, ReviewAdmin)
