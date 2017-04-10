from django.db import models
import datetime
from authentication.models import Profile
from django.contrib.auth.models import User

# Create your models here.
class VehicleCategory(models.Model):
	company_name = models.CharField(max_length=30)
	model = models.CharField(max_length=30)
	number_of_seats = models.IntegerField()
	number_of_doors = models.IntegerField()
	automatic_transmission = models.BooleanField(default=False)
	AC = models.BooleanField(default=False)
	per_Day_Charge = models.IntegerField(default=2400)
	per_Km_Charge = models.IntegerField(default=80)
	description = models.TextField(max_length=300)

	def __str__(self):
		return self.company_name+" "+self.model


class Vehicle(models.Model):
	vehicle_Category = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE)
	registartion_Number = models.CharField(max_length=30)
	odometer_Reading = models.IntegerField()
	available = models.BooleanField(default=True)

	def __str__(self):
		return str(self.vehicle_Category)+"( Reg No -"+self.registartion_Number+" )"


class Agency(models.Model):
	agency_name = models.CharField(max_length=30)
	noght_Halt_Charge = models.IntegerField(default=150)
	late_Panelty_Per_day = models.IntegerField(default=500)

	def __str__(self):
		return " Agency | "+self.name


class Booking(models.Model):
	user= models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
	odometer_Reading = models.IntegerField()
	return_Odometer_Reading = models.IntegerField(default=0)
	booking_Date = models.DateField(default=datetime.date.today)
	return_Date = models.DateField(default=datetime.date.today)
	actual_Return_Date = models.DateField(default=datetime.date.today)
	advance_Deposit = models.IntegerField(default=1000)
	payment_Number = models.IntegerField(default=0)
	payment_Amount = models.IntegerField(default=0)

	def __str__(self):
		return str(self.vehicle)+" | "+str(self.booking_Date)