from django.urls import path,include
from . import views

urlpatterns = [
    path('login', views.login, name='dashboard_login'),
    path('register', views.register, name='dashboard_register'),
    path('forgot-password', views.forgot_password, name='dashboard_forgot_password'),
    path('message', views.MessageConfirmEmail, name='dashboard_message_confirm_email'),
    path('pricing', views.Pricing, name='dashboard_pricing'),

    # ...
    path('', views.index, name='dashboard_index'),
    
    path('admins', views.get_admins, name='dashboard_admins'),
    
    
    #Clients
    path('clients', views.clients, name='dashboard_clients'),
    path('client/<int:client_id>', views.clients, name='dashboard_show_edit_client'),


    #Classes
    path('classes', views.classes, name='dashboard_classes'),
    path('class/<int:class_id>', views.classes, name='dashboard_edit_class'),


    #Enroll Requests
    path('enroll-requests', views.EnrollRequests, name='dashboard_enroll_requests'),
    path('enroll-requests/<int:client_id>', views.EnrollRequests, name='dashboard_confirm_enroll_requests'),


    #Students
    path('students', views.students, name='dashboard_students'),
    path('students/<int:student_id>', views.students, name='dashboard_edit_show_students'),
    path('add_students', views.get_student_form_add, name='dashboard_add_students'),


    path('pages/payments', views.get_payments, name='dashboard_payments'),
    path('pages/settings', views.settings_page, name='dashboard_settings'),
    path('pages/feedback', views.feedback_page, name='dashboard_feedback'),
]

urlpatterns += [
    path('auth/', include('django.contrib.auth.urls')),
]