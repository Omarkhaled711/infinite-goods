

from django import forms

from shop.models import ReviewRating


class ReviewRatingForm(forms.ModelForm):
    """
    A Review Rating form class for the Review Rating model
    """
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
