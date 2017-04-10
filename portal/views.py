from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from portal.models import VehicleCategory, Vehicle, Agency, Booking
from django.shortcuts import get_object_or_404
from portal.forms import BookingForm, UserEditForm, ProfileEditForm, ReturnForm
from django.contrib.auth.models import User
from authentication.models import Profile
import random
from django.contrib import messages
import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    return render(request,'portal/index.html',{'user':request.user})

@login_required
def book_vehicle(request,veh_id):
    vehicle = get_object_or_404(Vehicle, id=veh_id)
    if request.POST:
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.vehicle = vehicle
            booking.user = request.user
            booking.odometer_Reading = vehicle.odometer_Reading
            booking.save()
            vehicle.available = False
            vehicle.save()
            return redirect(reverse('login'))
    else:
        form = BookingForm()

    return render(request,'portal/book_vehicle.html',{'form':form,'veh':vehicle})

@login_required
def veh_filtered_list(request,pk):
    cat = get_object_or_404(VehicleCategory, id=pk)
    vehicles = Vehicle.objects.filter(vehicle_Category=cat)
    return render(request,'portal/vehicle_list.html',{'object_list':vehicles})

@login_required
def veh_cat_list(request,pk):
    cats = VehicleCategory.objects.all()
    return render(request,'portal/vehicle_list.html',{'object_list':cats,'user':request.user})

@login_required
def cat_info(request,pk):
    cat = get_object_or_404(VehicleCategory, id=pk)
    available_vehicles = Vehicle.objects.filter(vehicle_Category=cat,available=True)
    unavailable_vehicles = Vehicle.objects.filter(vehicle_Category=cat,available=False)
    return render(request,'portal/vehiclecategory_info.html',{'cat':cat, 'available_vehicles':available_vehicles,'unavailable_vehicles':unavailable_vehicles})

class VehCatList(ListView):
    model = VehicleCategory

class VehCatCreate(CreateView):
    model = VehicleCategory
    success_url = reverse_lazy('cat_list')
    # fields = ['name', 'ip', 'order']

class VehCatUpdate(UpdateView):
    model = VehicleCategory
    success_url = reverse_lazy('cat_list')
    # fields = ['name', 'ip', 'order']

class VehCatDelete(DeleteView):
    model = VehicleCategory
    success_url = reverse_lazy('cat_list')


@login_required
def veh_info(request,pk):
    veh = get_object_or_404(Vehicle, id=pk)
    try:
        booking = Booking.objects.filter(vehicle=veh).order_by('-id')[0]
        if booking.return_Odometer_Reading!=0:
            booking = None
    except:
        booking = None

    bookings = Booking.objects.filter(vehicle=veh).order_by('-id')

    return render(request,'portal/vehicle_info.html',{'veh':veh,'booking':booking,'object_list':bookings})

class VehList(ListView):
    model = Vehicle

class VehCreate(CreateView):
    model = Vehicle
    success_url = reverse_lazy('veh_list')
    fields = ['vehicle_Category', 'registartion_Number', 'odometer_Reading']

class VehUpdate(UpdateView):
    model = Vehicle
    success_url = reverse_lazy('veh_list')
    fields = ['vehicle_Category', 'registartion_Number', 'odometer_Reading']

class VehDelete(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('veh_list')



class AgencyUpdate(UpdateView):
    model = Agency
    success_url = reverse_lazy('home')


class BookingList(ListView):
    model = Booking

@login_required
def booking_list(request):
    if request.user.is_staff:
        object_list = Booking.objects.all()
    else:
        object_list = Booking.objects.filter(user=request.user)
    return render(request,'portal/booking_list.html',{'object_list':object_list})

@login_required
def booking_info(request,pk):
    booking = get_object_or_404(Booking, id=pk)
    return render(request,'portal/booking_info.html',{'booking':booking})

@login_required
def booking_return(request,pk):

    if request.POST:   
        returnform = ReturnForm(request.POST)

        if returnform.is_valid():
            booking = get_object_or_404(Booking, id=pk)

            if returnform.cleaned_data['odometer_Reading']<=booking.odometer_Reading:
                messages.add_message(request, messages.INFO, 'Invalid Odomoter Reading.')
                return redirect(reverse('booking_return',kwargs={'pk':booking.id}))

            booking.return_Odometer_Reading = returnform.cleaned_data['odometer_Reading']
            booking.actual_Return_Date = datetime.date.today()

            #payment policy
            agency_conf = Agency.objects.get(id=1)
            late_panelty = (booking.actual_Return_Date - booking.return_Date).days*agency_conf.late_Panelty_Per_day
            if late_panelty<0:
                late_panelty = 0
            day_charge = (booking.actual_Return_Date - booking.booking_Date).days*booking.vehicle.vehicle_Category.per_Day_Charge
            km_charge = (booking.return_Odometer_Reading - booking.odometer_Reading)*booking.vehicle.vehicle_Category.per_Km_Charge

            print(late_panelty)
            print(day_charge)
            print(km_charge)
            print(booking.advance_Deposit)

            booking.payment_Amount = late_panelty + day_charge + km_charge - booking.advance_Deposit

            booking.vehicle.odometer_Reading = booking.return_Odometer_Reading            
            booking.vehicle.available = True
            booking.vehicle.save()
            booking.save()
            return redirect(reverse('booking_info',kwargs={'pk':booking.id}))
    else:
        returnform = ReturnForm()    

    return render(request,'portal/booking_return.html',{'form':returnform})

@login_required
def booking_payment(request,pk):
    booking = get_object_or_404(Booking, id=pk)
    booking.payment_Number = random.randint(0,1000000)
    booking.save()
    
    return render(request,'portal/payment_redirect.html',{'id':booking.id})

@login_required
def profile_info(request,pk):
    user = get_object_or_404(User, id=pk)
    profile = get_object_or_404(Profile, user=user)
    bookings = Booking.objects.filter(user=user)
    return render(request,'portal/profile_info.html',{'profile':profile,'object_list':bookings})

@login_required
def profile_edit(request,pk):
    user = get_object_or_404(User, id=pk)
    profile = get_object_or_404(Profile, user=user)

    if user !=request.user and not request.user.is_staff:
        messages.add_message(request, messages.INFO, 'You can not edit others profile!.')
        return redirect(reverse('portal'))

    if request.POST:   
        userform = UserEditForm(request.POST,instance=user)
        userprofileform = ProfileEditForm(request.POST,instance=profile)

        if userform.is_valid() and userprofileform.is_valid():
            user = userform.save()
            userprofileform.save()
            return redirect(reverse('login'))
    else:
        userform = UserEditForm(instance=user)
        userprofileform = ProfileEditForm(instance=profile)
    
        return render(request,'portal/profile_edit.html',{'userform':userform,'userprofileform':userprofileform})