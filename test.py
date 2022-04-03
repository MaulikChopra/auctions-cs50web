from auctions.models import *
test_user = User.objects.last()
test_user2 = User.objects.first()

bat_listing = Listing(name="cricket bat", description="new cricket bat",
                      price=50, owner=test_user, category="cricket")
bat_listing.save()

bat_listing = Listing.objects.first()
new_comment = Comments(owner=test_user2, listing=bat_listing,
                       comment_content="very good condition")
new_comment.save()

new_bid = Bids(listing=bat_listing, owner=test_user2, bid_amount=60)
new_bid.save()
