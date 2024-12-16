from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['review_title', 'review_content', 'product_rating']

    def __init__(self, *args, **kwargs):
        """
        Add text-muted class
        """
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'text-muted my-2'
