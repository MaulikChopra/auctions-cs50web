from django import forms
from .models import Listing


class Create_listing_form(forms.Form):
    name = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": "25%", 'placeholder': 'Give a nice name...'}),
                           label="Name:", max_length=64, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "cols": "25%", 'placeholder': 'Describe your product...'}),
                                  label="Description:", required=True, max_length=1000)
    price = forms.FloatField(
        label="Price $:", required=True)
    category = forms.ChoiceField(
        choices=Listing.Categories.choices, required=True, label="Category:")
    image_url = forms.URLField(label="Image URL:", required=False)

    def __init__(self, *args, **kwargs):
        super(Create_listing_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'textfield'


class Create_bid_form(forms.Form):
    bid_amount = forms.FloatField(label="")

    def __init__(self, *args, **kwargs):
        super(Create_bid_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'textfield'


class Create_comment_form(forms.Form):
    comment_content = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": "25%", 'placeholder': 'Add a Comment...', "class": "comment-textfield"}),
                                      label="", required=True, max_length=1000)


class Category_form(forms.Form):
    category = forms.ChoiceField(
        choices=Listing.Categories.choices, required=True)
