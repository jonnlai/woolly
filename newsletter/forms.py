from django import forms
from .models import Subscriber

class SubscribeForm(forms.ModelForm):
    """ 
    Form class for user to subscribe to the newsletter
    """
    class Meta:
        model = Subscriber
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and remove auto-generated
        label
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'Email address',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False