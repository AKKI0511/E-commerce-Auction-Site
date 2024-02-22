from django.contrib import admin
from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "starting_bid", "is_closed")

    def is_closed(self, obj):
        return '✔' if not obj.closed else '❌'
    
    is_closed.short_description = 'Closed'

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "watchlist_length")

    def watchlist_length(self, obj):
        return obj.get_watchlist_length()
    
class CreatorAdmin(admin.ModelAdmin):
    list_display = ("creator", "listing")

    def creator(self, obj):
        return obj.user.username
    def listing(self, obj):
        return obj.listings_created

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "comment")

class BidAdmin(admin.ModelAdmin):
    list_display = ("bidder", "listing", "amount")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listings, ListingAdmin)
admin.site.register(ListingCreated, CreatorAdmin)
admin.site.register(Bids, BidAdmin)
admin.site.register(Comments, CommentAdmin)