from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# auth views :
def login(request):
    template = loader.get_template('auth/login.html')
    return HttpResponse(template.render())

def register(request):
    template = loader.get_template('auth/register.html')
    return HttpResponse(template.render())

def forgot_password(request):
    template = loader.get_template('auth/forgot-password.html')
    return HttpResponse(template.render())

# Create your views here.

@login_required
def index(request): 
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

@login_required
def get_admins(request):
    template = loader.get_template('admins/index.html')
    return HttpResponse(template.render())

@login_required
def get_clients(request):
    template = loader.get_template('users/index.html')
    return HttpResponse(template.render())

@login_required
def get_enroll_requests(request):
    template = loader.get_template('users/enroll_requests.html')
    return HttpResponse(template.render())

@login_required
def get_payments(request):
    template = loader.get_template('pages/payments.html')
    return HttpResponse(template.render())

@login_required
def settings_page(request):
    template = loader.get_template('pages/settings.html')
    return HttpResponse(template.render())

@login_required
def feedback_page(request):
    template = loader.get_template('pages/feedback.html')
    return HttpResponse(template.render())
