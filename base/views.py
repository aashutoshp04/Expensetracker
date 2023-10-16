from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.db.models import Q
# Create your views here.
def loginview(request):
    
    if request.user.is_authenticated:
        return redirect('employees')

    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            context ={'user': user}
            return redirect(reverse('employees'),context)
        
        messages.error(request,"Invalid credentials")
        return render(request,"login.html")

    return render(request,"login.html")

@login_required(login_url='login')
def logoutview(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def EmployeeView(request):
    try:
        employees = Employee.objects.all()
        context = {
            ''
            'employees' : employees
        }
    except:
        pass
    return render(request,'employees.html',context)

@login_required(login_url='login')
def EmployeeProfileView(request,pk):
    flight_budget=0
    travel_budget=0
    ope_budget=0
    employee=0
    try:
        employee = Employee.objects.get(uuid=pk)
        print(employee)
        flight_budget = FlightBudget.objects.get(employee=employee)
        travel_budget = TravelBudget.objects.get(employee=employee)
        ope_budget = OPEBudget.objects.get(employee=employee)
    except:
        pass
    context = {
        'employee': employee,
        'flight_budget' : flight_budget,
        'travel_budget' : travel_budget,
        'ope_budget' : ope_budget
    }
    return render(request,"profile.html",context)

@login_required(login_url='login')
def AdvancedTravelPlanView(request,pk):
    try:
        emp = Employee.objects.get(uuid=pk)
        print(emp)
        atp = AdvancedTravelPlan.objects.filter(employee=emp)
        
    except:
        atp = None

    context = {
        'atp' : atp,
        'emp' : emp
    }
    print(atp)
    return render(request,"advancedtravelplan.html",context)


@login_required(login_url='login')
def Search(request):
    search_query = request.GET.get('search_query')

    if search_query:
        employ = Employee.objects.filter( Q(Emp_name__icontains=search_query) | Q(contract_no__icontains=search_query))
    else:
        employ = Employee.objects.all()
    context = {
        'employ': employ,
        'search_query': search_query,
        }
    return render(request,'employees.html',context)
        
