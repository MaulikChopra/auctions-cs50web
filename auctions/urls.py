from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:entry>/", views.listing_page, name="listing_pages"),
    path("listing/<str:entry>/create_new_bid",
         views.create_new_bid, name="create_new_bid"),
    path("listing/<str:entry>/close_listing",
         views.close_listing, name="close_listing"),
    path("watchlist", views.watchlist_page, name="watchlist"),
    path("category", views.category_page_index, name="category"),
    path("category/<str:category_name>/",
         views.specific_category_page, name="specific_category"),
    path("my_listings", views.my_listings_page, name="my_listings")
]
