from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Employee, Role, Department
import datetime
from django.db.models import Q
from django.http import Http404


# Create your views here.
def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'view_all_emp.html', context=context)


def add_emp(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone,
                           dept_id=dept, role_id=role, hire_date=datetime.datetime.now())
        new_emp.save()
        return redirect(to='all_emp')
    elif request.method == "GET":
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An Exception Occured!")


def remove_emp(request, emp_id=-1):
    if emp_id > 0:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except:
            return HttpResponse("Error while processing!")

    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context=context)


def filter_emp(request):
    if request.method == "POST":
        filters = []
        name = request.POST["name"]
        dept = request.POST["dept"]
        role = request.POST["role"]
        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
            filters.append("Name")
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
            filters.append("Department")
        if role:
            emps = emps.filter(role__name__icontains=role)
            filters.append("Role")

        context = {
            'emps': emps,
            "filters": filters
        }
        return render(request, 'view_all_emp.html', context)
    elif request.method == "GET":
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse("An error occured!")


def edit_emp(request, emp_id: int):
    employeeProfile = get_object_or_404(Employee, id=emp_id)
    if request.method == "POST":
        # employeeProfile = get_object_or_404(Employee, id=emp_id)
        employeeProfile.first_name = request.POST["first_name"]
        employeeProfile.last_name = request.POST["last_name"]
        employeeProfile.phone = int(request.POST["phone"])
        employeeProfile.save()
        return redirect(to="all_emp")
    elif request.method == "GET":
        context = {'emp':employeeProfile}
        return render(request, "update_emp.html", context=context)


