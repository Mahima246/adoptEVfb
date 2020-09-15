from django.db import models


# Create your models here.

# this model Stores the data of the Phones Verified
class phoneModel(models.Model):
    Mobile = models.IntegerField(blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)   # For HOTP Verification

    def __str__(self):
        return str(self.Mobile)


class profile(models.Model):
    name = models.CharField(max_length=100)
    ph_no =models.CharField(max_length=12)
    email_address = models.CharField(max_length=200)
    company_name = models.CharField(max_length=150)
    GST_no = models.CharField(max_length=25)
    Address=models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    State = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # def __str__
