from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from userApp.models import *
from core.models import *
from .decorators import *
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


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



#clients
@login_required
def clients(request, client_id=None):
    if client_id is not None:
        
        if request.method == 'GET':
            user = User.objects.filter(id=client_id).values()
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
            role = Role.objects.filter(name__in=['employee', 'business client', 'customer']).values_list('id', flat=True) 
            users = User.objects.filter(role__in=role).values()
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
            role = Role.objects.filter(name__in=['employee', 'business client', 'customer']).values_list('id', flat=True) 
            users = User.objects.filter(role__in=role, is_active = 0).values()
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
