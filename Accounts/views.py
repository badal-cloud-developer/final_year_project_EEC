from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Household, Organization, Metro
from django.contrib.auth import login,authenticate,logout


User = get_user_model()


def entry(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Corrected line
            role = user.role
            if role == 'household':
                return redirect('waste_report')
            elif role == 'metro':
                return redirect("waste_status")
            elif role == 'organization':
                return redirect('requests')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
        
    return render(request, 'login.html')


def sign_up(request):
    wards = range(1, 30)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', '').strip()

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        try:
            user = User.objects.create(
                username=username,
                password=make_password(password),
                role=role
            )

            # Role-specific data
            if role == 'household':
                name = request.POST.get('name')
                house_no = request.POST.get('house_no')
                municipal = request.POST.get('municipal')
                ward_no = int(request.POST.get('wardno'))
                Household.objects.create(
                    user=user,
                    name=name,
                    house_no=house_no,
                    municipal=municipal,
                    ward_no=ward_no
                )

            elif role == 'organization':
                org_name = request.POST.get('org_name')
                ward_no = int(request.POST.get('ward_no'))
                waste_type = request.POST.get('waste_type')
                Organization.objects.create(
                    user=user,
                    org_name=org_name,
                    ward_no=ward_no,
                    waste_type=waste_type
                )

            elif role == 'metro':
                metro_name = request.POST.get('metro_name')
                Metro.objects.create(
                    user=user,
                    metro_name=metro_name
                )

            

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('signup')

    return render(request, 'signup.html', {'wards': wards})

def logout_view(request):
    logout(request)
    return redirect('login')
