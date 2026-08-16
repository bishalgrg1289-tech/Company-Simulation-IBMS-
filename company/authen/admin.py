import django
from django.contrib import admin

from authen.models import Employee, Task

# Register your models here.

django.contrib.admin.site.register(Employee)
django.contrib.admin.site.register(Task)