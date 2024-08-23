from rest_framework.pagination import PageNumberPagination 

class DefaultPagination(PageNumberPagination):
    page_size = 5
    

# class UserPagination(PageNumberPagination):
#     page_size = 2   


class AddressPagination(PageNumberPagination):
    page_size = 1