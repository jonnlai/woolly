from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Subscriber, Newsletter


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')

    ordering = ('-date_subscribed',)

class NewsletterAdmin(SummernoteModelAdmin):

    list_display = ('subject', 'date_created')
    search_fields = ['subject']
    
    ordering = ('-date_created',)



admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
