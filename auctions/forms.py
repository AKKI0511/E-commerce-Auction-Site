from django import forms
from .models import *

#Class of a form to create a New entry 
class CreateForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

# Form for new bid value
class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['amount']

# Form for new comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

# Form for category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['category']
        exclude = ['title', 'description', 'starting_bid', 'image']
