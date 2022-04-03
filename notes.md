To get all fields of table or model: User.\_meta.get_fields()
or User.\_meta.fields

To get data using specific querys use: User.objects.get(parameters)

parameters: the specified columns of table.
eg: pk, username, etc

category = categories.NAME_OF_CATEGORY
category label= categories.NAME_OF_CATEGORY.label

Datetime saved as django.utils.timezone.now, saves in UTC.

Access it using:

listing = Listing.objects.get(pk="2")

t = listing.datetime_created.year/month/day/hour/minute/second/tzinfo

FORMS IN DJANGO
https://www.geeksforgeeks.org/django-forms/

NULL object is NONE
