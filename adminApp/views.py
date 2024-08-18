from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from userApp.models import *
from core.models import *
from .decorators import *



def access_admin_page(role_id):
    role_names = Role.objects.filter(id=role_id).values_list('name', flat=True)
    
    role_names = list(role_names)  # تحويل نتيجة الاستعلام إلى قائمة
    
    if 'admin' in role_names or 'super admin' in role_names:
        # يتم التحقق من وجود دور "admin" أو "super admin"
        return True
    else:
        return False


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
    role_business_client = Role.objects.filter(name__in=['business client', 'costomer']).values_list('id', flat=True) 
    role_costomer = Role.objects.filter(name__in=['costomer']).values_list('id', flat=True) 

    count_business_client_users = User.objects.filter(role__in=role_business_client).count()
    count_role_costomer_users = User.objects.filter(role__in=role_costomer).count()

    context = {'count_business_client_users': count_business_client_users,
               'count_role_costomer_users': count_role_costomer_users
            }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


@login_required
# @role_required('admin', 'super admin')
def get_admins(request):
    if access_admin_page(request.user.role_id):
        role = Role.objects.filter(name__in=['admin', 'super admin']).values_list('id', flat=True) 
        admis = User.objects.filter(role__in=role).values()
        admis_list = list(admis)
        
        context = {'admis_list': admis_list}
        template = loader.get_template('admins/index.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse('cant access to this page')


@login_required
def get_clients(request):
    role = Role.objects.filter(name__in=['employee', 'business client', 'costomer']).values_list('id', flat=True) 
    users = User.objects.filter(role__in=role).values()
    users_list = list(users)
    # return HttpResponse(users_list)
    context = {'users_list': users_list}
    template = loader.get_template('users/index.html')
    return HttpResponse(template.render(context, request))




# classes
@login_required
def get_classes(request):
    user = request.user
    classes = Classes.objects.filter(user=user).values()  
    classes_list = list(classes)
    
    # Convert classes_list to a dictionary to pass as context
    context = {'classes_list': classes_list}
    
    template = loader.get_template('classes/index.html')
    return HttpResponse(template.render(context, request))

@login_required
def add_class(request):
    # return HttpResponse(" request method")
    if request.method == 'POST':
        
        class_name = request.POST['class_name']
        user = request.user
        
        new_class = Classes()
        new_class.name = class_name
        new_class.user = user
        new_class.save()
        
        return HttpResponse(f"Class '{class_name}' added successfully!")
    return HttpResponse("Invalid request method")
    # template = loader.get_template('users/classes/add-class.html')
    # return HttpResponse(template.render())




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
