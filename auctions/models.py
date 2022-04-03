from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator


class User(AbstractUser):
    def __str__(self):
        return f"id:{self.id}, username:{self.username}, email:{self.email}"


class Listing(models.Model):

    class Categories(models.TextChoices):
        HOME = 'Home Products', _('Home Products')
        FASHION_BEAUTY = 'Fashion & Beauty', _('Fashion & Beauty')
        TOYS_GAMES = 'Toys & Games', _('Toys & games')
        ELECTRONICS = 'Electronics', _('Electronics')
        AUTOMOTIVE = 'Automotive', _('Automotive')
        BOOKS = 'Books', _('Books')
        CELLPHONES = 'Cell Phones & Accessories', _(
            'Cell Phones & Accessories')
        CLOTHING_SHOES = 'Clothing & Shoes', _('Clothing & Shoes')
        COMPUTERS = 'Computers', _('Computers')
        COLLECTIBLES_FINEART = 'Collectibles & Fine Arts', _(
            'Collectibles & Fine Arts')
        HANDMADE = 'Handmade', _('Handmade')
        HEALTH = 'Health & Fitness', _('Health & Fitness')
        SPORTS_OUTDOORS = 'Sports & Outdoors', _('Sports & Outdoors')
        OFFICE_PRODUCTS = 'Office Products', _('Office Products')
        REAL_ESTATE = 'Real Estate', _('Real Estate')
        OTHER = 'Others', _('Others')

    # id is automatically created
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    price = models.FloatField(validators=[MinValueValidator(1)])
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    category = models.CharField(
        max_length=64, choices=Categories.choices)
    image_url = models.URLField(null=True, blank=True)
    datetime_created = models.DateTimeField()
    listing_closed = models.BooleanField(default=False)
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="auctions_won")

    def __str__(self):
        return f"id:{self.id}, name:{self.name}, price:{self.price}, owner:{self.owner.username}, category:{self.category}"


class Bids(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.FloatField(validators=[MinValueValidator(1)])
    datetime_created = models.DateTimeField()

    def __str__(self):
        return f"id:{self.id}, bid_amount:{self.bid_amount}, listing:({self.listing}), owner:({self.owner})"


class Comments(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")
    comment_content = models.CharField(max_length=1000)
    datetime_created = models.DateTimeField()

    def __str__(self):
        return f"id:{self.id}, comment_content:{self.comment_content}, listing:({self.listing}), owner:({self.owner})"


class Watchlist(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watched_by")

    def __str__(self):
        return f"id:{self.id}, owner:({self.owner}), listing:({self.listings})"
