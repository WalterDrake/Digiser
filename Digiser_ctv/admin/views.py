from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from authentication.models import CustomUser, LoginLog
from django.contrib.auth.models import Group
from home.utils import *

# Create your views here.

@login_required
@user_passes_test(checkManager)
def home_admin(request):
    return render(request, 'admin/home_admin.html')


@login_required
@user_passes_test(checkManager)
def ctv_list(request):
    context = {
        'users': CustomUser.objects.prefetch_related('groups').only('code', 'full_name', 'status'),
        'status_choices': CustomUser._STATUSES,
        'groups': Group.objects.all(),
    }
    return render(request, 'admin/ctv_list.html', context)

@login_required
@user_passes_test(checkManager)
def list_loginlog(request):
    loginlogs = LoginLog.objects.all()
    return render(request, 'admin/login_log.html', {'loginlogs': loginlogs})

