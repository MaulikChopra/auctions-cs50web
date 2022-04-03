from .models import *
from django.utils import timezone


def store_data_in_listing_model(formdata, username):
    try:
        Listing(
            name=formdata['name'],
            description=formdata['description'],
            price=formdata['price'],
            owner=User.objects.get(username=username),
            category=Listing.Categories(formdata["category"]),
            image_url=formdata['image_url'],
            datetime_created=timezone.now()
        ).save()
        print('SUCCESS: saved to database')
        return 0
    except Exception as e:
        print(e)
        return -1


def store_data_in_bids_model(bid_amount, owner, listing):
    try:
        Bids(
            listing=listing,
            owner=owner,
            bid_amount=bid_amount,
            datetime_created=timezone.now()
        ).save()
        print('SUCCESS: saved to database')
        return 0
    except Exception as e:
        print(e)
        return -1


def update_close_listing_model(listing, winner):
    try:
        listing.listing_closed = True
        listing.winner = winner
        listing.save()
        return 0
    except Exception as e:
        print(e)
        return -1


def store_comment_in_model(data, owner, listing):
    try:
        Comments(owner=owner,
                 listing=listing,
                 comment_content=data['comment_content'],
                 datetime_created=timezone.now()
                 ).save()
        return 0
    except Exception as e:
        print(e)
        return -1


def add_to_watchlist_model(owner, listing):
    try:
        Watchlist(owner=owner,
                  listings=listing
                  ).save()
        return 0
    except Exception as e:
        print(e)
        return -1


def remove_from_watchlist_model(owner, listing):
    try:
        owner.watchlist.filter(listings__exact=listing).delete()
        return 0
    except Exception as e:
        print(e)
        return -1


def filter_url(entry):
    id = ""
    for i in entry.strip():
        if i == "_":
            break
        id += i
    return id
