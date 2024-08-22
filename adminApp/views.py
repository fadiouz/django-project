from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from userApp.models import *
from core.models import *
from .models import *

from .decorators import *
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone


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
    template = loader.get_template('registration/login.html')
    return HttpResponse(template.render())

def register(request):
    context = {}
    
    if request.method == "GET":
        # role = Role.objects.filter(name__in=['customer', 'business account']).values() 
        # context = {'role_list': role}
        template = loader.get_template('registration/register.html')
        
    elif request.method == "POST":
        User = get_user_model()
        current_datetime = timezone.now()
        username = request.POST.get('username')
        email = request.POST.get('email')
        role_id = request.POST.get('role')
        subscriptionInfo_id = request.POST.get('subscriptionInfo')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        selected_role = get_object_or_404(Role, pk=role_id)
        selected_SubscriptionInfos = get_object_or_404(SubscriptionInfos, pk=subscriptionInfo_id)
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        
        
        user = User.objects.create_user(username=username, email=email, password=password, phone_number=phone_number, role=selected_role, is_active=False)
        Subscriptions.objects.create(user=user, subscriptionInfo=selected_SubscriptionInfos, start_date=formatted_date, end_date=formatted_date)

        return redirect('dashboard_message_confirm_email') 

    return HttpResponse(template.render(context, request))
    
def forgot_password(request):
    template = loader.get_template('registration/forgot-password.html')
    return HttpResponse(template.render())


def MessageConfirmEmail(request):
    template = loader.get_template('registration/message_confirm_email.html')
    return HttpResponse(template.render())


def RegistrationPricing(request, role_id):
    pricing_list = SubscriptionInfos.objects.filter(role=role_id).values('id', 'type' ,'max_employee_numbers', 'max_request_rate', 'price', 'role__name', 'role__id')
    context = {'pricing_list': pricing_list,
                       }
    
    template = loader.get_template('registration/pricing.html')
    return HttpResponse(template.render(context, request))
# Create your views here.


def RegistrationSelect(request):
    role = Role.objects.filter(name__in=['customer', 'business account']).values() 
    context = {'role_list': role}
    
    template = loader.get_template('registration/select_role.html')
    return HttpResponse(template.render(context, request))
# Create your views here.


def RegistrationMain(request):
    template = loader.get_template('registration/main.html')
    return HttpResponse(template.render())



@login_required
def index(request): 
    role_business_account = Role.objects.filter(name__in=['business account']).values_list('id', flat=True) 
    # return HttpResponse(role_business_client)
    role_customer_business_account = Role.objects.filter(name__in=['customer', 'business account']).values_list('id', flat=True) 

    count_business_account_client = User.objects.filter(role__in=role_business_account).count()
    count_customer_business_account_client = User.objects.filter(role__in=role_customer_business_account).count()

    context = {'count_business_account_client': count_business_account_client,
               'count_customer_business_account_client': count_customer_business_account_client
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



#clients
@login_required
def clients(request, client_id=None):
    if client_id is not None:
        
        if request.method == 'GET':
            user = User.objects.filter(id=client_id).values('username', 'email' ,'phone_number' ,'is_active', 'id', 'role__name')
            user_list = list(user)
            context = {'user_list': user_list}
            template = loader.get_template('users/show.html')
            
        elif request.method == 'POST':
            is_active = request.POST.get('is_active') 
            user = User.objects.get(id=client_id)  
            user.is_active = is_active
            user.save()
            return redirect('dashboard_clients') 
         
         
    elif client_id is None:  
        
        if request.method == 'GET':
            role = Role.objects.filter(name__in=['business account', 'customer']).values_list('id', flat=True) 
            users = User.objects.filter(role__in=role, is_active = 1).values('username', 'email' ,'phone_number' ,'is_active', 'id', 'role__name')
            users_list = list(users)
            context = {'users_list': users_list}
            template = loader.get_template('users/index.html')
 
    return HttpResponse(template.render(context, request))


# classes
@login_required
def classes(request, class_id=None):
    if class_id is None:
        if request.method == 'GET':
            user = request.user
            classes = Classes.objects.filter(user=user).values()  
            classes_list = list(classes)
            context = {'classes_list': classes_list}
            template = loader.get_template('classes/index.html')
            
        elif request.method == 'POST':
            class_name = request.POST['class_name']
            user = request.user
            new_class = Classes()
            new_class.name = class_name
            new_class.user = user
            new_class.save()
            return redirect('dashboard_classes')
        
    elif class_id is not None:
        
        if request.method == 'POST':
            class_name = request.POST['class_name']
            old_class = Classes.objects.get(id=class_id)  
            old_class.name = class_name
            old_class.save()
            return redirect('dashboard_classes')
        
    return HttpResponse(template.render(context, request))


#Enroll Requests
@login_required
def EnrollRequests(request, client_id=None):
    if client_id is not None: 
        user = User.objects.get(id=client_id)  
        user.is_active = 1
        user.save()
        return redirect('dashboard_enroll_requests') 
         
         
    elif client_id is None:  
        if request.method == 'GET':
            role = Role.objects.filter(name__in=['business account', 'customer']).values_list('id', flat=True) 
            users = User.objects.filter(role__in=role, is_active = 0).values('username', 'email', 'role__name', 'is_active', 'id')
            users_list = list(users)
            context = {'users_list': users_list}
            template = loader.get_template('users/enroll_requests.html')

    return HttpResponse(template.render(context, request))



#Students
@login_required
def students(request, student_id=None):
    if student_id is None:
        if request.method == 'GET':
            user = request.user
            class_ids = Classes.objects.filter(user=user).values_list('id', flat=True)
            students = StudentClasses.objects.filter(classes__in=class_ids).select_related('student').values('student__first_name', 'student__last_name', 'student__father', 'student__mother', 'classes__name', 'classes__id', 'student__id', 'examination_id', 'date')
            context = {'students_list': students}
            template = loader.get_template('students/index.html')
        
        if request.method == 'POST':
            f_name = request.POST['f_name']
            l_name = request.POST['l_name']
            father_name = request.POST['father_name']
            mother_name = request.POST['mother_name']
            examination_id = request.POST['examination_id']
            date = request.POST['date']
            Class_id  = request.POST.get('Class') 
            selected_class = get_object_or_404(Classes, pk=Class_id)
            # return HttpResponse(Class)
            
            new_student = Students()  
            new_student.first_name = f_name
            new_student.last_name = l_name
            new_student.father = father_name
            new_student.mother = mother_name
            new_student.save()
            
            
            new_student_classes = StudentClasses()
            new_student_classes.classes = selected_class
            new_student_classes.examination_id = examination_id
            new_student_classes.date = date
            new_student_classes.student = new_student
            new_student_classes.save()
            
            

            return redirect('dashboard_students')
            
            
    elif student_id is not None:
        if request.method == 'GET':
            user = request.user
            classes = Classes.objects.filter(user=user).values()
            students_list = StudentClasses.objects.filter(student=student_id).select_related('student').values('student__first_name', 'student__last_name', 'student__father', 'student__mother', 'classes__name', 'classes__id', 'student__id', 'examination_id', 'date')
            context = {'students_list': students_list,
                       'classes': classes
                       }
            template = loader.get_template('students/show_edit.html')


        if request.method == 'POST':
            f_name = request.POST['f_name']
            l_name = request.POST['l_name']
            father_name = request.POST['father_name']
            mother_name = request.POST['mother_name']
            examination_id = request.POST['examination_id']
            date = request.POST['date']
            Class_id  = request.POST.get('Class') 
            selected_class = get_object_or_404(Classes, pk=Class_id)
            # return HttpResponse(Class)
            old_student_classes = StudentClasses.objects.get(student=student_id)  
            old_student_classes.classes = selected_class
            old_student_classes.examination_id = examination_id
            old_student_classes.date = date
            old_student_classes.save()
            
            old_student = Students.objects.get(id=student_id)  
            old_student.first_name = f_name
            old_student.last_name = l_name
            old_student.father = father_name
            old_student.mother = mother_name
            old_student.save()

            return redirect('dashboard_students')
        
        
    return HttpResponse(template.render(context, request) if template else 'No template found')


@login_required
def get_student_form_add(request):
    user = request.user
    classes = Classes.objects.filter(user=user).values()
    
    context = {'classes': classes
            }
    
    template = loader.get_template('students/add.html')
    return HttpResponse(template.render(context, request))



#pricing
@login_required
def Pricing(request, pricing_id=None):
    if pricing_id is None:
        if request.method == "GET":
            pricing = SubscriptionInfos.objects.values('id', 'type' ,'max_employee_numbers', 'max_request_rate', 'price', 'role__name', 'role__id')
            context = {'pricing_list': pricing,   
                         
                    }
            template = loader.get_template('pricing/index.html')
            
        if request.method == 'POST':
            type = request.POST['type']
            max_employee = request.POST['max_employee']
            max_request = request.POST['max_request']
            price = request.POST['price']
            role_id  = request.POST.get('role') 
            selected_role = get_object_or_404(Role, pk=role_id)
            
            new_pricing = SubscriptionInfos()  
            new_pricing.type = type
            new_pricing.max_employee_numbers = max_employee
            new_pricing.max_request_rate = max_request
            new_pricing.price = price
            new_pricing.role = selected_role
            new_pricing.save()
            
            return redirect('dashboard_pricing')
    
    elif pricing_id is not None:
        if request.method == 'GET':
            role = Role.objects.filter(name__in=['customer', 'business account']).values() 
            pricing_list = SubscriptionInfos.objects.filter(id=pricing_id).values('id', 'type' ,'max_employee_numbers', 'max_request_rate', 'price', 'role__name', 'role__id')
            context = {'pricing_list': pricing_list,
                       'role_list': role
                       }
            template = loader.get_template('pricing/show_edit.html')


        if request.method == 'POST':
            type = request.POST['type']
            max_employee = request.POST['max_employee']
            max_request = request.POST['max_request']
            price = request.POST['price']
            role_id  = request.POST.get('role') 
            selected_role = get_object_or_404(Role, pk=role_id)
            
            old_pricing = SubscriptionInfos.objects.get(id=pricing_id)  
            old_pricing.type = type
            old_pricing.max_employee_numbers = max_employee
            old_pricing.max_request_rate = max_request
            old_pricing.price = price
            old_pricing.role = selected_role
            old_pricing.save()

            return redirect('dashboard_pricing') 
    return HttpResponse(template.render(context, request) if template else 'No template found')


@login_required
def get_pricing_form_add(request):
    role = Role.objects.filter(name__in=['customer', 'business account']).values() 
    context = {'role_list': role}
    
    template = loader.get_template('pricing/add.html')
    return HttpResponse(template.render(context, request))




#employee
@login_required
def employees(request, employee_id=None):
    user = request.user
    if user.role.name == 'business account':
        if employee_id is not None:
            
            if request.method == 'GET':
                employee = User.objects.filter(id=employee_id).values('username', 'email' ,'phone_number' ,'is_active', 'id', 'role__name')
                employee_list = list(employee)
                context = {'employee_list': employee_list}
                template = loader.get_template('employee/show_edit.html')
                
            elif request.method == 'POST':
                is_active = request.POST.get('is_active') 
                employee_name = request.POST['employee_name'] 
                employee_number_phone = request.POST['employee_number_phone'] 

                employee = User.objects.get(id=employee_id)
                employee.username = employee_name
                employee.phone_number = employee_number_phone
                employee.is_active = is_active
                employee.save()
                return redirect('dashboard_employees') 
            
            
        elif employee_id is None:  
            
            if request.method == 'GET':
                user = request.user
                # role = Role.objects.filter(name__in=['employee']).values_list('id', flat=True) values('username', 'email' ,'phone_number' ,'is_active', 'id', 'role__name')
                employee_ids = Employees.objects.filter(user=user).values_list('employee', flat=True)
                employees = User.objects.filter(id__in=employee_ids).values('username', 'email' ,'phone_number' ,'is_active', 'id', 'role__name')
                employees_list = list(employees)
                context = {'employees_list': employees_list}
                template = loader.get_template('employee/index.html')

            if request.method == 'POST':
                user = request.user
                role = Role.objects.get(name='employee')
                is_active = request.POST.get('is_active') 
                employee_name = request.POST['employee_name'] 
                employee_number_phone = request.POST['employee_number_phone'] 
                email = request.POST['email'] 
                employee_password = request.POST['employee_password'] 

                employee = User.objects.create_user(username=employee_name, email=email, password=employee_password, phone_number=employee_number_phone, role=role, is_active=is_active)
                Employees.objects.create(user=user, employee=employee)
                        
                return redirect('dashboard_employees') 
    else:
        return redirect('dashboard_error') 
    return HttpResponse(template.render(context, request))

@login_required
def get_employees_form_add(request):
    user = request.user
    context = {'user': user}
    template = loader.get_template('employee/add.html')
    return HttpResponse(template.render(context, request))


def Error(request):
    user = request.user
    context = {'user': user}
    template = loader.get_template('error/error-403.html')
    return HttpResponse(template.render(context, request))



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
