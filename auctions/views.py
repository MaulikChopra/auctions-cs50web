from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from .forms import *
from .models import User, Listing
from . import util
from django.db.models import Max


def index(request):
    active_listings = Listing.objects.filter(
        listing_closed=False).order_by("-datetime_created")
    closed_listings = Listing.objects.filter(
        listing_closed=True).order_by("-datetime_created")

    return render(request, "auctions/index.html", {
        'listings': active_listings,
        "closed_listings": closed_listings
    })


def listing_page(request, entry):
    id = util.filter_url(entry)
    listing = Listing.objects.get(pk=id)
    bids = listing.bids.all()
    top_bid = bids.aggregate(Max('bid_amount'))['bid_amount__max']
    # No bids till now

    show_bid_button, show_close_button, add_to_watchlist, show_winner = True, False, True, False
    if request.user.username == listing.owner.username:
        show_bid_button = False
        show_close_button = True
    if listing.winner is not None:
        if request.user.username == listing.winner.username:
            show_winner = True
    if len(listing.bids.all()) == 0:
        show_close_button = False
    try:
        if request.user.watchlist.get(listing__exact=listing):
            add_to_watchlist = False  # show remove from watchlist
    except Exception:
        add_to_watchlist = True
    # POST METHODS
    if request.method == 'POST':
        comment_form = None
        if request.POST.get("add_watchlist") == "":
            if util.add_to_watchlist_model(request.user, listing) == 0:
                return HttpResponseRedirect(request.path_info)
            else:
                return render(request, "auctions/error.html", {
                    "error_content": "Cannot save to database"
                })

        if request.POST.get("remove_watchlist") == "":
            if util.remove_from_watchlist_model(request.user, listing) == 0:
                return HttpResponseRedirect(request.path_info)
            else:
                return render(request, "auctions/error.html", {
                    "error_content": "Cannot delete from database"
                })
        if request.POST.get("add_comment") == "":
            comment_form = Create_comment_form(request.POST)
            if comment_form.is_valid():
                data = comment_form.cleaned_data
                success = util.store_comment_in_model(
                    data, request.user, listing)
                if success == 0:
                    return HttpResponseRedirect(request.path_info)
                else:
                    return render(request, "auctions/error.html", {
                        "error_content": "Cannot save to database"
                    })

    else:
        if request.user.is_authenticated:
            comment_form = Create_comment_form()
        else:
            comment_form = None
    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "bids": listing.bids.order_by("-datetime_created"),
        "comments": listing.comments.order_by("-datetime_created"),
        "show_bid_button": show_bid_button,
        "show_close_button": show_close_button,
        "add_to_watchlist": add_to_watchlist,
        "show_winner": show_winner,
        "comment_form": comment_form,
        "top_bid": top_bid
    })


@login_required
def watchlist_page(request):
    lists = request.user.watchlist.all().order_by("-listing")
    return render(request, "auctions/watchlist.html", {
        "lists": lists
    })


@login_required
def my_listings_page(request):
    active_listings = request.user.listings.filter(
        listing_closed=False).order_by("-datetime_created")
    closed_listings = request.user.listings.filter(
        listing_closed=True).order_by("-datetime_created")

    return render(request, "auctions/index.html", {
        'listings': active_listings,
        "closed_listings": closed_listings
    })


@login_required
def create_new_bid(request, entry):
    id = util.filter_url(entry)
    listing = Listing.objects.get(pk=id)
    bids = listing.bids.all()
    top_bid = bids.aggregate(Max('bid_amount'))['bid_amount__max']
    # No bids till now
    if top_bid is None:
        top_bid = listing.price
        owner_of_top_bid = None
    elif top_bid is not None:
        owner_of_top_bid = listing.bids.get(bid_amount=top_bid).owner

    if request.method == 'POST':
        form = Create_bid_form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['bid_amount'] > top_bid:
                stored = util.store_data_in_bids_model(
                    data["bid_amount"], request.user, listing)
                if stored == -1:
                    return render(request, "auctions/error.html", {
                        "error_content": "Cannot save to database"
                    })
                return HttpResponseRedirect("./")
            return render(request, "auctions/create_new_bid.html", {
                "form": form,
                "top_bid": top_bid,
                "owner_of_top_bid": owner_of_top_bid,
                "error": True
            })
    else:
        if request.user.is_authenticated:
            form = Create_bid_form()
        else:
            return render(request, "auctions/error.html", {
                "error_content": "UnAuthorized: Please Login"
            })

    return render(request, "auctions/create_new_bid.html", {
        "form": form,
        "top_bid": top_bid,
        "owner_of_top_bid": owner_of_top_bid
    })


def close_listing(request, entry):
    id = util.filter_url(entry)
    listing = Listing.objects.get(pk=id)
    bids = listing.bids.all()
    # find top bid from all bids on listing
    top_bid = bids.aggregate(Max('bid_amount'))['bid_amount__max']
    # No bids till now
    if top_bid is None:
        top_bid = listing.price
        owner_of_top_bid = None
    if top_bid is not None:
        #   without .owner this is the winning_bid
        owner_of_top_bid = listing.bids.get(bid_amount=top_bid).owner

    if request.method == 'POST':
        if request.POST.get("ACCEPTED") == "":
            if owner_of_top_bid is not None:
                success = util.update_close_listing_model(
                    listing, owner_of_top_bid)
                if success == 0:
                    return HttpResponseRedirect("./")
                else:
                    return render(request, "auctions/error.html", {
                        "error_content": "Cannot save to database"
                    })

            else:
                return render(request, "auctions/close_listing.html", {
                    "top_bid": top_bid,
                    "owner_of_top_bid": owner_of_top_bid,
                    "error": "There are no Top Bids by any user."
                })

            # MAKE THE LISTING INACTIVE USING MODELS
    return render(request, "auctions/close_listing.html", {
        "top_bid": top_bid,
        "owner_of_top_bid": owner_of_top_bid
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


def create_listing(request):
    if request.method == 'POST':
        form = Create_listing_form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # CORNER CASES FOR DATA
            if data['image_url'] == '':
                data['image_url'] = None
            if data['category'] == None:
                return render(request, 'auctions/createlisting.html', {
                    'form': form,
                    "error": "Please select a category"
                })
            if data['price'] < 1:
                return render(request, 'auctions/createlisting.html', {
                    'form': form,
                    "error": "Please enter price greater than $1"
                })

            # STORE TO DATABASE AND RETURN TO INDEX
            saved = util.store_data_in_listing_model(
                data, request.user.username)
            if saved == -1:
                return render(request, "auctions/error.html", {
                    "error_content": "Cannot save to database"
                })
            return HttpResponseRedirect(reverse("index"))

    # if a GET (or any other method) we'll create a blank form
    else:
        if request.user.is_authenticated:
            form = Create_listing_form()
        else:
            return render(request, "auctions/error.html", {
                "error_content": "UnAuthorized: Please Login"
            })

    return render(request, 'auctions/createlisting.html', {
        'form': form
    })


def specific_category_page(request, category_name):
    c = category_name.strip()
    listings = Listing.objects.filter(
        category=Listing.Categories(c), listing_closed=False).order_by("-datetime_created")
    closed_listings = Listing.objects.filter(
        category=Listing.Categories(c), listing_closed=True).order_by("-datetime_created")

    return render(request, "auctions/index.html", {
        "listings": listings,
        "closed_listings": closed_listings
    })


def category_page_index(request):
    categories = Listing.Categories
    return render(request, "auctions/category.html", {
        "categories": categories
    })
