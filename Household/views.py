from django.shortcuts import render,redirect,get_object_or_404
from common.decorators import role_required
from .models import WasteReport,IllegalDumping,Like
from django.contrib import messages
from .forms import ProfilePhotoForm
from .models import UserProfile


# Create your views here.
@role_required(allowed_roles=['household'])
def waste_report(request):
    if request.method == 'POST':
        try:
            # Get basic fields
            waste_type = request.POST.get('waste_type', '').strip().lower()
            items = request.POST.getlist('items[]')
            quantities = request.POST.getlist('quantities[]')
            description = request.POST.get('description', '').strip()
            location = request.POST.get('location', '').strip()
            status = request.POST.get('status', 'pending').strip()

            item_list = []

            # Validate items and quantities
            for item, qty in zip(items, quantities):
                item = item.strip()
                if item and qty:
                    try:
                        quantity = float(qty)
                        item_list.append({'item': item, 'quantity': quantity})
                    except ValueError:
                        continue  # Skip if quantity is not a valid number

            # Calculate points based on waste type
            waste_points = {
                'organic': 5,
                'nonorganic': 3,
                'ewaste': 10
            }
            points = waste_points.get(waste_type, 0) * len(item_list)

            # Save the report
            WasteReport.objects.create(
                user=request.user,
                waste_type=waste_type,
                items=item_list,
                description=description,
                location=location,
                status=status,
                points=points
            )

            messages.success(request, "Your waste report has been submitted successfully!")
            return redirect('waste_report')

        except Exception as e:
            messages.error(request, f"Error submitting report: {str(e)}")
            return redirect('waste_report')

    return render(request, 'report.html')

@role_required(allowed_roles=['household'])
def illegal_dumping(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            description = request.POST.get('description')
            area = request.POST.get('area')
            photo = request.FILES.get('photo')  
            

            # Save to database
            IllegalDumping.objects.create(
                user=request.user,
                description=description,
                Area=area,
                picture=photo
            )

            messages.success(request, "Your illegal report has been submitted successfully!")
            return redirect('illegal_report')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('illegal_report')

    return render(request,'illegal.html')
    

    

@role_required(allowed_roles=['household'])
def household_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = ProfilePhotoForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('household_profile')

    illegal_dumps = IllegalDumping.objects.filter(user=request.user).order_by('-report_time')
    waste_reports = WasteReport.objects.filter(user=request.user).order_by('-report_time')
    waste_points = sum(w.points for w in waste_reports)
    illegal_report_point=sum(w.points for w in illegal_dumps)
    total_point=waste_points+illegal_report_point
    context={
        'form': form,
        'profile': profile,
        'illegal_dumps': illegal_dumps,
        'waste_reports': waste_reports,
        'points':total_point
    }
    return render(request,'household_profile.html',context)

@role_required(allowed_roles=['household'])
def household_notification(request):
    illegal_dumps = IllegalDumping.objects.filter(user=request.user).order_by('-report_time')  # descending order
    waste_reports = WasteReport.objects.filter(user=request.user).order_by('-report_time')  
    context = {
        'illegal_dumps': illegal_dumps,
        'waste_reports': waste_reports,
    }
    return render(request, 'household_notification.html', context)  

@role_required(allowed_roles=['household'])
def map_view(request):
    return render(request,'map.html')
@role_required(allowed_roles=['household'])
def all_reports(request):
    reports = IllegalDumping.objects.all().order_by('-report_time')
    user_likes = Like.objects.filter(user=request.user) if request.user.is_authenticated else []
    liked_ids = [like.report.id for like in user_likes]
    return render(request, 'all_reports.html', {
        'reports': reports,
        'liked_ids': liked_ids
    })

@role_required(allowed_roles=['household'])
def like_report(request, report_id):
    report = get_object_or_404(IllegalDumping, id=report_id)
    like, created = Like.objects.get_or_create(user=request.user, report=report)
    if not created:
        like.delete()  # Unlike
    return redirect('all_reports')
