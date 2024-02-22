from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

# Database of all the users with all the listings in their watchlist
class User(AbstractUser):
    watchlist = models.ManyToManyField('Listings', blank=True)

    def __str__(self) -> str:
        return f"{self.username}"

    def get_watchlist_length(self):
        return len(self.watchlist.all())

# Database for all info about a listing
class Listings(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Books', 'Books'),
        # Add more categories as needed
    ]

    title = models.CharField(max_length=96)
    description = models.TextField()
    starting_bid = models.IntegerField() # Which is also the current highest bid
    image = models.ImageField(upload_to='images/', blank=True)
    closed = models.BooleanField(default=False)  # Add a 'closed' field
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Electronics')

    
    def __str__(self) -> str:
        return f"{self.id}: {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((300, 300))  # Adjust the size as needed
            img.save(self.image.path)

    # Function that closes listing and sets the highest bidder as the winner
    def close_listing(self):
        if not self.closed:
            self.closed = True
            highest_bid = self.bids.order_by("-amount").first()
            if highest_bid:
                self.winner = highest_bid.bidder
            self.save()

    def get_highest_bid_amount(self):
        highest_bid = self.bids.aggregate(models.Max('amount'))
        return highest_bid['amount__max'] if highest_bid['amount__max'] is not None else 0
    
    def get_all_comments(self):
        comments = self.comments.all()
        return comments

# Database for every new listing that is created 
class ListingCreated(models.Model):
    listings_created = models.ManyToManyField('Listings', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Creator: {self.user.username}"

# Database for every new bid from a logged-in user
class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()

    def __str__(self) -> str:
        return f"Bid #{self.id} - Listing: {self.listing.title}, Bidder: {self.bidder.username}, Amount: ${self.amount}"

# Database for all the comments for a perticular listing
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self) -> str:
        return f"#{self.id} - Listing: {self.listing.title}, User: {self.user.username}, Comment: {self.comment}"