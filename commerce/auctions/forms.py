from django import forms
from .models import AuctionListing, Bid, Comment, Category

class AuctionListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False, empty_label="Select Category")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'price', 'image_url', 'category'  ]

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'content']
