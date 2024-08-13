from django_seed import Seed
from .models import *
import random  
from django.utils import timezone  
from django.contrib.auth.hashers import make_password  

seeder = Seed.seeder()


seeder.add_entity(Role, 10, {
    'name': lambda x: seeder.faker.user_name(),
})
seeder.execute()


# seeder.add_entity(User, 1, {
#     'username': "superadmin",
#     'email': "superadmin@superadmin.com",
#     'phone_number': None,
#     'password': make_password("superadmin1234"),  
#     'is_superuser': False,
#     'is_staff': False,
#     'is_active': True,
#     'date_joined': lambda x: timezone.now(),
#     'role': '1'
# })

# seeder.execute()

# users = User.objects.all()
# addresses = Addresses.objects.all()


# for user in users:
#     for address in addresses:
#         business_account = BusinessAccounts.objects.create(user=user, name=seeder.faker.user_name())
#         business_account.address.set([address])


# business_accounts = BusinessAccounts.objects.all()

# for user in users:
#     for business_account in business_accounts:
#         employee = Employees.objects.create(user=user, business_accounts=business_account, first_name=seeder.faker.user_name(), last_name=seeder.faker.user_name())


# for user in users:
#     for address in addresses:
#         customer = Customers.objects.create(user=user, first_name=seeder.faker.user_name(), last_name=seeder.faker.user_name())
#         customer.address.set([address])        
