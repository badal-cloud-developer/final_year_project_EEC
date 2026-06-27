from django.shortcuts import render,get_object_or_404,redirect
from common.decorators import role_required
from common.functions import haversine_distance_time,get_street_location,send_whatsapp_message
from Household.models import WasteReport
from Accounts.models import Organization
from .models import OrganizationProfile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .forms import ProfilePhotoForm
from django.db.models import Count, Sum, Avg, Max
from django.contrib import messages
from django.conf import settings

# Create your views here.


@role_required(allowed_roles=['organization'])
def get_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        
        #  Save to session
        request.session['receiver_lat'] = latitude
        request.session['receiver_lon'] = longitude

        print(f" Saved in session → Lat: {latitude}, Lon: {longitude}")
        return JsonResponse({"status": "success", "lat": latitude, "lon": longitude})

    return JsonResponse({"status": "error"}, status=400)
@role_required(allowed_roles=['organization'])
def requests_view(request):
    get_location(request)
    user_type = request.user.organization.waste_type

    if user_type == 'Degradable':
        reports = WasteReport.objects.filter(status='pending', waste_type='organic')
    elif user_type == 'Non-degradable':
        reports = WasteReport.objects.filter(status='pending', waste_type='nonorganic')
    elif user_type == 'E-waste':
        reports = WasteReport.objects.filter(status='pending', waste_type='ewaste')
    else:
        reports = WasteReport.objects.none()

    #  Get receiver location from session
    lat2 = request.session.get('receiver_lat')
    lon2 = request.session.get('receiver_lon')

    for report in reports:
        try:
            lat1, lon1 = map(str.strip, report.location.split(','))
            report.lat = lat1
            report.lng = lon1

            if lat1 and lon1 and lat2 and lon2:
                distance, time = haversine_distance_time(
                    float(lat1), float(lon1),
                    float(lat2), float(lon2)
                )
                report.distance = distance
                report.eta_minutes = time
                report.area=get_street_location(lat1,lon1)
            else:
                report.distance = None
                report.eta_minutes = None
        except Exception:
            report.lat = ''
            report.lng = ''
            report.distance = None
            report.eta_minutes = None
            report.area=None

    context = {'reports': reports}
    return render(request, 'requests.html', context)


@role_required(allowed_roles=['organization'])
def accepted_requests(request):
    user_type = request.user.organization.waste_type
    
    if user_type == 'Degradable':
        reports = WasteReport.objects.filter(status='accepted', waste_type='organic')
    elif user_type == 'Non-degradable':
        reports = WasteReport.objects.filter(status='accepted', waste_type='nonorganic')
    elif user_type == 'E-waste':
        reports = WasteReport.objects.filter(status='accepted', waste_type='ewaste')
    else:
        reports = WasteReport.objects.none()


   #  Get receiver location from session
    lat2 = request.session.get('receiver_lat')
    lon2 = request.session.get('receiver_lon')

    for report in reports:
        try:
            lat1, lon1 = map(str.strip, report.location.split(','))
            report.lat = lat1
            report.lng = lon1

            if lat1 and lon1 and lat2 and lon2:
                distance, time = haversine_distance_time(
                    float(lat1), float(lon1),
                    float(lat2), float(lon2)
                )
                report.distance = distance
                report.eta_minutes = time
                report.area=get_street_location(lat1,lon1)
            else:
                report.distance = None
                report.eta_minutes = None
        except Exception:
            report.lat = ''
            report.lng = ''
            report.distance = None
            report.eta_minutes = None
            report.area=None

    context = {'reports': reports}
    return render(request, 'accepted_requests.html', context)

@role_required(allowed_roles=['organization'])
def route_view(request):
    org_name = request.user.organization.org_name
    accepted_reports = WasteReport.objects.filter(status='accepted', collected_by=org_name)
    print("objects", accepted_reports)

    locations = []
    for report in accepted_reports:
        try:
            lat, lng = map(float, report.location.split(','))
            locations.append([lat, lng])
        except Exception as e:
            print(f"Error parsing location for report {report.id}: {e}")
            continue
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'locations': locations
    }
    
    return render(request, 'route.html',context )



@role_required(allowed_roles=['organization'])
def profile_view(request):
    profile, created = OrganizationProfile.objects.get_or_create(user=request.user)
    form = ProfilePhotoForm(request.POST or None, request.FILES or None,instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('receiver_profile')
    organization_name=request.user.organization.org_name
    reports=WasteReport.objects.filter(collected_by=organization_name)
    reports = WasteReport.objects.filter(collected_by=organization_name)
    
    total_pickups = reports.count()
    total_points = reports.aggregate(total=Sum('points'))['total'] or 0
    last_collection = reports.aggregate(latest=Max('collected_at'))['latest']
    if total_points==0 and total_points==0:
        average_points_per_pickup=0
    else:
        average_points_per_pickup = total_points/total_pickups or 0
    

    

    #total waste collected in kg
    total_quantity = 0
    for report in reports:
        for item in report.items:
            total_quantity += float(item.get('quantity', 0))
    
    progress_percentage = (total_quantity / 1000) * 100
    if total_points==0 and total_points==0:
        average_waste_per_pickup=0
    else:
        average_waste_per_pickup = total_quantity/total_pickups or 0

    context = {
        'organization_name': organization_name,
        'total_pickups': total_pickups,
        'total_points': total_points,
        'last_collection': last_collection,
        'average_points_per_pickup': round(average_points_per_pickup, 2),
        'average_waste_per_pickup': round(average_waste_per_pickup, 2),
        'total_quantity': round(total_quantity, 2),
        'progress_percentage': round(progress_percentage, 2),
        'form': form,
    }
    
    
    return render(request,'receiver_profile.html',context)

@role_required(allowed_roles=['organization'])
def accept_request(request, report_id):
    report = get_object_or_404(WasteReport, id=report_id)
    report.status = 'accepted'
    report.collected_by = request.user.organization.org_name
    report.save()
    
    # Redirect to the 'requests' URL
    return redirect('requests')


@role_required(allowed_roles=['organization'])
def accept_request(request, report_id):
    report = get_object_or_404(WasteReport, id=report_id)
    report.status = 'accepted'
    report.collected_by = request.user.organization.org_name
    report.save()
    
    # Redirect to the 'requests' URL
    return redirect('requests')


def send_notification_whatsapp(request):
    if request.method == 'POST':
        organization_name = request.user.organization.org_name
        reports = WasteReport.objects.filter(collected_by=organization_name, status='accepted')
        
        numbers =set( [report.user.username for report in reports] ) # phone numbers
        print("numbers_______________",numbers)
        message = f"""Hello! from {organization_name},
Your waste collection is scheduled for tomorrow at 8:00 AM. 
Please plan your schedule accordingly.
"""
        send_whatsapp_message(numbers, message)

        messages.success(request, "WhatsApp notifications sent to all users with accepted reports.")
        return redirect('accepted_requests')
    
    return redirect('accepted_requests')


    

    
    
