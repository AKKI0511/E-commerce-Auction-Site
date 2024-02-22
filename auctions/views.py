from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# Create New listing function
def create_listing(request):
    if request.method == "POST":
        user = request.user
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = form.save()  # Save the listing and get the instance
            creator = ListingCreated(user=user)
            creator.save()
            creator.listings_created.set([new_listing])  # Use .set() for many-to-many relationship
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/index.html",{
            "Create_Listing": True,
            "form": CreateForm()
        })

# Listing function
def listing(request, listing_id):
    user = request.user
    error_messages = None
    exists_in_watchlist = False

    # Get listing details from listing_id
    listing = Listings.objects.get(id=listing_id)
    creator = ListingCreated.objects.get(listings_created=listing)
    current_user_is_creator = (user == creator.user)

    # Only if user is loged-in, check if that listing exists in their watchlist
    if user.is_authenticated:
        watchlist = user.watchlist.all()
        exists_in_watchlist = True if listing in watchlist else False

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():

            # Get the new bid from the user
            amount = form.cleaned_data["amount"]

            # If bid is valid, change the bid in the database
            if amount > listing.get_highest_bid_amount() and amount > listing.starting_bid:
                listing.starting_bid = amount
                listing.save()
                new_bid = Bids(listing=listing, bidder=user, amount=amount)
                new_bid.save()

            # Else show error message
            else:
                error_messages = "Please bid higher than the current bid"
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_form": BidForm(),
            "error_message": error_messages,
            "exists_in_watchlist": exists_in_watchlist,
            "creator": creator.user,
            "current_user_is_creator": current_user_is_creator,
            "comment_form": CommentForm(),
            "all_comments": listing.get_all_comments()
        })

# Watchlist function
def watchlist(request):
    if request.method == "POST":

        # Get the watchlist of the user who is logged-in
        user = request.user
        watchlist = user.watchlist.all()

        # Get listing which user wants to add/remove
        listing_id = request.POST["add"]
        listing = Listings.objects.get(id=listing_id)

        # If listing not already in watchlist: add it else remove
        if listing not in watchlist:
            user.watchlist.add(listing)
        else:
            user.watchlist.remove(listing)
        user.save()
    return render(request, "auctions/watchlist.html")


# Function to close a Listing done by the creator
def close(request):
    if request.method == "POST":

        # Get listing which the logged-in user wants to close
        listing_id = request.POST["close"]
        listing = Listings.objects.get(id=listing_id)

        # Close listing
        listing.close_listing()
    return redirect("listing", listing_id=listing_id)


# Function to save new comments
def comment(request):
    if request.method == "POST":

        # Get the form posted by the user and the listing-id in which the form is submitted
        form = CommentForm(request.POST)
        listing_id = request.POST["cmt"]
        listing = Listings.objects.get(id=listing_id)
        if form.is_valid():

            # Get the comment written by the loged-in user
            comment = form.cleaned_data['comment']

            # Add the new comment to database ( with values of the user commenting and the listing )
            new_comment = Comments(user=request.user, comment=comment, listing=listing)
            new_comment.save()
        return redirect("listing", listing_id=listing_id)

def category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            listings = Listings.objects.filter(category=form.cleaned_data["category"])
            return render(request, "auctions/category.html", {
                "category_form": form,
                "category_listings": listings
            })
    return render(request, "auctions/category.html", {
        "category_form": CategoryForm()
    })