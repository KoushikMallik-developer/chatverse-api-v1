from django.db import models


class AccountType(models.TextChoices):
    REGULAR = "regular", "Regular"
    SELLER = "seller", "Seller"
    ADMIN = "admin", "Admin"
    STAFF = "staff", "Staff"
