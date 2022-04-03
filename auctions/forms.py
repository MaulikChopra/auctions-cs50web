from django import forms
from .models import Listing


class Create_listing_form(forms.Form):
    name = forms.CharField(
        label="Name", max_length=128, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 60}),
                                  label="Description", required=True, max_length=1000)
    price = forms.FloatField(
        label="Price $", required=True)
    category = forms.ChoiceField(
        choices=Listing.Categories.choices, required=True)
    image_url = forms.URLField(
        label="Image URL", required=False)


class Create_bid_form(forms.Form):
    bid_amount = forms.FloatField(label="Price: $")


class Create_comment_form(forms.Form):
    comment_content = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "cols": 100}),
                                      label="Comment", required=True, max_length=1000)


class Category_form(forms.Form):
    category = forms.ChoiceField(
        choices=Listing.Categories.choices, required=True)
