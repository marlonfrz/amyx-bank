from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def transactions(request):
    pass

@login_required
def transfer(request):
    pass

@login_required
def commissions(request):
    pass

@login_required
def buy(request):
    pass