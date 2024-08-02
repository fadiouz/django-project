from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Count
from MyApp.models import User, Address
# Create your views here.

def say_hello(request):
    
    # user = Address.objects.filter(id__in = Address.objects.values('address'))
    # user = User.objects.filter(address__in = Address.objects.values('id').filter(street = 'damas'))
    
    #### to fech num of user in a adderss
    # user = Address.objects.annotate(num = Count('user')) 

    #####  gt main grater than  ||  gte main grater than or ==
    # user = User.objects.filter(id__gt = 0).first() 
    
    
    #####  اختبار قيمة حقل بقيمة حقل اخر
    # user = User.objects.filter(f_name = F('l_name')).first()
    
    #####   to revers the value we can use function revers or use (-) befor the value of order_by
    # user = User.objects.order_by('f_name').reverse().first()
    # user = User.objects.order_by('-f_name').first()


    ##### (and)  to but to filter ther are 3 way
    # user = User.objects.filter(f_name__contains = 'fadi', l_name__contains = 'asali').first() 
    # user = User.objects.filter(f_name__contains = 'fadi').filter(l_name__contains = 'asali').first() 
    # user = User.objects.filter(Q(f_name__contains = 'fadi') & Q(l_name__contains = 'asali')).first() 


    ##### (or)  to but to filter ther are to way
    # user = User.objects.filter(Q(f_name__contains = 'fadi') | Q(l_name__contains = 'asali')).first() 
    # user = User.objects.filter(f_name__contains = 'fadi').filter(l_name__contains = 'asali').first() 


    ##### to create new row in data base
    # user = User()
    # user.f_name = 'roni'
    # user.l_name = 'asali'
    # user.phone = '09822sd227656'
    # user.address = Address(pk=1)
    # user.email = 'roni_asali22s2@gmail.com'
    # user.save()

    # user = User(id=3)
    # user.f_name = 'roni'
    # user.l_name = 'asali'
    # user.phone = '09822sd227656'
    # user.address = Address(pk=1)
    # user.email = 'roni_asali22s2@gmail.com'
    # user.save()
    
    ##### other way to update
    # User.objects.filter(id=1).delete()
    
    
    return render(request, 'login.html')
