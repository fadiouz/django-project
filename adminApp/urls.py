from django.urls import path,include
from . import views

urlpatterns = [
    path('login', views.login, name='dashboard_login'),
    path('register', views.register, name='dashboard_register'),
    path('forgot-password', views.forgot_password, name='dashboard_forgot_password'),

    # ...
    path('', views.index, name='dashboard_index'),
    path('admins', views.get_admins, name='dashboard_admins'),
    path('clients', views.get_clients, name='dashboard_clients'),
    
    # classes
    path('client/classes', views.get_classes, name='dashboard_client_classes'),
    path('client/add-class', views.form_add_class, name='dashboard_client_form_add_class'),

    path('enroll-requests', views.get_enroll_requests, name='dashboard_enroll_requests'),
    path('pages/payments', views.get_payments, name='dashboard_payments'),
    path('pages/settings', views.settings_page, name='dashboard_settings'),
    path('pages/feedback', views.feedback_page, name='dashboard_feedback'),
]

urlpatterns += [
    path('auth/', include('django.contrib.auth.urls')),
]