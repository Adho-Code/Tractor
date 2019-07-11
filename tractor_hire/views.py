from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .email import send_welcome_email
from django.core.exceptions import ObjectDoesNotExist
import datetime

# Create your views here.
def index(request):
    tractors = Tractor.fetch_all_tractors()
    location = Location.get_location()
    current_date = datetime.datetime.now()
    return render(request,'tractor_hire/index.html',{"tractors":tractors,"locations":location,"current_date":current_date})

def search_category(request):
    if 'category' in request.GET and request.GET ["category"]:
        search_term = request.GET.get("category")
        searched_tractors = Tractor.search_tractor(search_term)
        message = f'{search_term}'

        return render(request, 'search/search.html', {"message":message, "searched_tractors":searched_tractors})

    else:
        message = "No search results yet!"
        return render (request, 'search/search.html', {"message": message})

@login_required(login_url='/accounts/login/')
def tractor_details(request,tractor_id):
    if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                user_email = form.cleaned_data['user_email']
                recipient = Event(start_date=start_date,user_email=user_email)
                recipient.save()
                send_welcome_email(start_date,user_email)
                HttpResponseRedirect('index')
                print('Valid')
    else:
        form = BookingForm()
    single_tractor = Tractor.get_single_tractor(tractor_id)
    return render(request,'tract_hire/tractor_details.html',{"single_tractor":single_tractor,"bookingForm":form})

def filter_by_location(request,tractor_id):
    try:
        location = Location.get_location()
        located_tractors = Tractor.objects.filter(location_id=tractor_id)
    except DoesNotExist:
        raise Http404()
    return render(request,'tractor_location/filter_location.html',{"located_tractors":located_tractors,"locations":location})

@login_required(login_url='/accounts/login/')
def new_tractor(request):
    current_user = request.user
    if request.method == 'POST':
        form = TractorForm(request.POST,request.FILES)
        if form.is_valid():
            user_tractor = form.save(commit=False)
            user_tractor.user = current_user
            user_tractor.save()
        return redirect('index')
    else:
        form = TractorForm()
    return render(request,"upload_tractor/new_tractor.html",{"form":form})

@login_required(login_url='/accounts/login/')
def new_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.prof_user = current_user
            profile.profile_Id = request.user.id
            profile.save()
        return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'profile/new_profile.html', {"form": form})

@login_required(login_url='/accounts/login/')
def profile_edit(request):
    current_user = request.user
    if request.method == 'POST':
        logged_user = Profile.objects.get(prof_user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=logged_user)
        if form.is_valid():
            form.save()
        return redirect('profile')
    else:
        form = ProfileForm()
    return render(request,'profile/edit_profile.html',{'form':form})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    tractors = Tractor.objects.filter(user = current_user)

    try:   
        prof = Profile.objects.get(prof_user=current_user)
    except ObjectDoesNotExist:
        return redirect('new_profile')

    return render(request,'profile/profile.html',{'profile':prof,'tractors':tractors})

