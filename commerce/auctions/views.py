from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import AuctionListing, Bid, Comment
from .forms import AuctionListingForm, BidForm, CommentForm

def index(request):
    active_listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })

#@login_required
def create_listing(request):
    if request.method == "GET":
        form = AuctionListingForm(request.GET)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.is_active = True
            listing.save()
            return redirect('index')
    else:
        form = AuctionListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })

@login_required
def watchlist(request):
    user = request.user
    watchlist_items = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

def listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    user = request.user
    is_owner = user == listing.owner
    is_watching = user.is_authenticated and listing in user.watchlist.all()
    highest_bid = listing.bids.order_by('-amount').first()

    bid_form = BidForm()
    comment_form = CommentForm()

    if request.method == "POST":
        if "watchlist" in request.POST:
            if is_watching:
                user.watchlist.remove(listing)
            else:
                user.watchlist.add(listing)
            return redirect('listing', listing_id=listing_id)

        elif "bid" in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                if bid.amount <= listing.starting_bid or (highest_bid and bid.amount <= highest_bid.amount):
                    messages.error(request, "Your bid must be higher than the current bid.")
                else:
                    bid.listing = listing
                    bid.bidder = user
                    bid.save()
                    return redirect('listing', listing_id=listing_id)

        elif "close" in request.POST and is_owner:
            listing.is_active = False
            listing.save()
            return redirect('listing', listing_id=listing_id)

        elif "comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.listing = listing
                comment.commenter = user
                comment.save()
                return redirect('listing', listing_id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_owner": is_owner,
        "is_watching": is_watching,
        "highest_bid": highest_bid,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "comments": listing.comments.all()
    })

def login_view(request):
    # Implementação da função de login
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    # Implementação da função de logout
    logout(request)
    return redirect('index')

def register(request):
    # Implementação da função de registro
    pass

def categories(request):
    categories = AuctionListing.objects.values_list('category', flat=True).distinct()
    return render(rquest, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category):
    listings = AuctionListing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })
