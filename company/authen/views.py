
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CustomUserCreationForm, SubmissionForm, TaskForm
from .models import Employee, Task


def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        Employee.objects.create(user=user)
        login(request, user)
        return redirect('dash_board_view')
    return render(request, 'websites/register.html', {'form': form})


def login_view(request):
    error_message = None
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('dash_board_view')
        error_message = 'Invalid username or password.'
    return render(request, 'websites/login.html', {'error_message': error_message})


@login_required
def dash_board_view(request):
    employee = get_object_or_404(Employee, user=request.user)
    if employee.status == 'admin':
        tasks = Task.objects.select_related('assigned_to__user')
        employees = Employee.objects.filter(status='employee').select_related('user')
    else:
        tasks = employee.tasks.all()
        employees = []
    return render(request, 'websites/dashboard.html', {
        'employee': employee, 'tasks': tasks, 'employees': employees,
    })


@login_required
def create_task_view(request):
    employee = get_object_or_404(Employee, user=request.user)
    if employee.status != 'admin':
        raise Http404
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.assigned_by = request.user
        task.save()
        return redirect('dash_board_view')
    return render(request, 'websites/task_form.html', {'form': form})


@login_required
def submit_task_view(request, task_id):
    employee = get_object_or_404(Employee, user=request.user)
    task = get_object_or_404(Task, id=task_id, assigned_to=employee)
    if task.status == 'finished':
        return redirect('dash_board_view')
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=task)
    else:
        form = SubmissionForm(instance=task)
    if form.is_valid():
        task = form.save(commit=False)
        task.status = 'submitted'
        task.submitted_at = timezone.now()
        task.save(update_fields=('submission', 'status', 'submitted_at'))
        return redirect('dash_board_view')
    return render(request, 'websites/task_submit.html', {'form': form, 'task': task})


@login_required
def verify_task_view(request, task_id):
    employee = get_object_or_404(Employee, user=request.user)
    if employee.status != 'admin':
        raise Http404
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST' and task.status == 'submitted':
        task.status = 'finished'
        task.verified_at = timezone.now()
        task.save(update_fields=('status', 'verified_at'))
    return redirect('dash_board_view')


def logout_view(request):
    logout(request)
    return redirect('home')