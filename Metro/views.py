from django.shortcuts import render
from common.decorators import role_required
from Household.models import WasteReport,IllegalDumping,Like
import json
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from Household.models import IllegalDumping
from .models import Vehicle
from django.db.models import Q
from .forms import VehicleForm


# Create your views here.
@role_required(allowed_roles=['metro'])
def waste_status(request):
    def process_reports(queryset, report_type):
        processed = []
        for report in queryset:
            lat, lng = map(float, report['location'].split(','))
            processed.append({
                'lat': lat,
                'lng': lng,
                'type': report_type,  # 'degradable', 'recyclable', or 'nonDegradable'
                'desc': report['items'][0].get('item'),
                'quantity': report['items'][0].get('quantity'),
                'description': report['description']
            })
        return processed

    organic_reports = process_reports(
        WasteReport.objects.filter(waste_type='organic',status='pending').values('items', 'location', 'description'),
        'degradable'
    )
    nonorganic_reports = process_reports(
        WasteReport.objects.filter(waste_type='nonorganic',status='pending').values('items', 'location', 'description'),
        'recyclable'
    )
    ewaste_reports = process_reports(
        WasteReport.objects.filter(waste_type='ewaste',status='pending').values('items', 'location', 'description'),
        'nonDegradable'
    )

    all_reports = organic_reports + nonorganic_reports + ewaste_reports

    return render(request, 'waste_status.html', {
        'waste_reports_json': json.dumps(all_reports)  # Serialize for JavaScript
    })
@role_required(allowed_roles=['metro'])
@role_required(allowed_roles=['metro'])
def vehicle_details(request):
    vehicles = Vehicle.objects.all()
    search_query = request.GET.get('search', '')
    ward_filter = request.GET.get('ward_filter')

    if search_query:
        vehicles = vehicles.filter(
            Q(driver_name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(bus_no__icontains=search_query)
        )
    if ward_filter:
        vehicles = vehicles.filter(ward_no=ward_filter)

    form = VehicleForm()
    wards = Vehicle.objects.values_list('ward_no', flat=True).distinct()

    if request.method == 'POST':
        if 'save_vehicle' in request.POST:
            form = VehicleForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('vehicle_details')

        elif 'update_vehicle' in request.POST:
            vehicle_id = request.POST.get('vehicle_id')
            vehicle = get_object_or_404(Vehicle, id=vehicle_id)
            form = VehicleForm(request.POST, instance=vehicle)
            if form.is_valid():
                form.save()
                return redirect('vehicle_details')

    if 'edit' in request.GET:
        vehicle = get_object_or_404(Vehicle, id=request.GET.get('edit'))
        form = VehicleForm(instance=vehicle)
        return render(request, 'vehicles_details.html', {
            'vehicles': vehicles,
            'form': form,
            'edit_id': vehicle.id,
            'wards': wards,
            'search_query': search_query,
            'ward_filter': ward_filter
        })

    if 'delete' in request.GET:
        vehicle = get_object_or_404(Vehicle, id=request.GET.get('delete'))
        vehicle.delete()
        return redirect('vehicle_details')

    return render(request, 'vehicles_details.html', {
        'vehicles': vehicles,
        'form': form,
        'wards': wards,
        'search_query': search_query,
        'ward_filter': ward_filter
    })

@role_required(allowed_roles=['metro'])
def waste_graph(request):
    return render(request,'waste_graphs.html')
@role_required(allowed_roles=['metro'])
def user_recyclers(request):
    return render(request,'user_recyclers.html')
@role_required(allowed_roles=['metro'])
def schedule(request):
    return render(request,'schedule.html')
@role_required(allowed_roles=['metro'])
def illegal_dumping(request):
    reports = IllegalDumping.objects.all().order_by('-report_time')
    user_likes = Like.objects.filter(user=request.user) if request.user.is_authenticated else []
    liked_ids = [like.report.id for like in user_likes]
    return render(request, 'illegal_dumping.html', {
        'reports': reports,
        'liked_ids': liked_ids
    })
@role_required(allowed_roles=['metro'])
def cost_estimation(request):
    return render(request,'cost_estimation.html')
@role_required(allowed_roles=['metro'])
def Profile(request):
    return render(request,'profile.html')

def update_dumping_status(request, pk):
    report = get_object_or_404(IllegalDumping, pk=pk)

    if request.method == "POST":
        new_status = request.POST.get("status")

        # Is the option valid?
        if new_status in dict(IllegalDumping.STATUS_CHOICES):
            report.status = new_status
            report.save()

            # A canned message that matches the choice
            msg_map = {
                IllegalDumping.STATUS_PENDING:"marked as pending again",
                IllegalDumping.STATUS_PROCESSING: "Marked as under processing.",
                IllegalDumping.STATUS_VALIDATED:  "Evidence checked – report validated ✔️",
                IllegalDumping.STATUS_INVALID:    "Report reviewed and marked invalid.",
            }
            messages.success(request, msg_map[new_status])
        else:
            messages.error(request, "Invalid status option.")

    # pop back to the list (or wherever they came from)
    return redirect(request.META.get("HTTP_REFERER", "illegal_dumping"))

